import math
import re

import numpy as np
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


_sbert_model = None


def normalize_similarity(similarity):
    """Normalize similarity scores to a safe range between 0 and 1."""
    if similarity is None:
        return 0.0

    try:
        value = float(similarity)
    except (TypeError, ValueError):
        return 0.0

    if math.isnan(value) or math.isinf(value):
        return 0.0

    return max(0.0, min(1.0, value))


def safe_text(text):
    if text is None:
        return ""
    return str(text).strip()


def basic_clean(text):
    """Lowercase + remove punctuation. Used for Jaccard/TF-IDF/Word2Vec.
    NOT used for SBERT, which needs natural sentence structure."""
    text = safe_text(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def _get_sbert_model():
    global _sbert_model
    if _sbert_model is None:
        try:
            _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            return None
    return _sbert_model


def jaccard_similarity(reference_text, student_text):
    reference_text = safe_text(reference_text)
    student_text = safe_text(student_text)
    if not reference_text or not student_text:
        return 0.0

    set1 = set(basic_clean(reference_text).split())
    set2 = set(basic_clean(student_text).split())
    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0.0

    return normalize_similarity(len(intersection) / len(union))


def tfidf_similarity(reference_text, student_text):
    reference_text = safe_text(reference_text)
    student_text = safe_text(student_text)
    if not reference_text or not student_text:
        return 0.0

    docs = [basic_clean(reference_text), basic_clean(student_text)]
    if not any(docs):
        return 0.0

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(docs)
    except ValueError:
        return 0.0

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return normalize_similarity(float(score))


def word2vec_similarity(reference_text, student_text):
    reference_text = safe_text(reference_text)
    student_text = safe_text(student_text)
    if not reference_text or not student_text:
        return 0.0

    ref_tokens = basic_clean(reference_text).split()
    stu_tokens = basic_clean(student_text).split()
    if not ref_tokens or not stu_tokens:
        return 0.0

    try:
        sentences = [ref_tokens, stu_tokens]
        model = Word2Vec(sentences, vector_size=50, window=5, min_count=1, workers=1, epochs=50)
    except Exception:
        return 0.0

    def avg_vector(tokens):
        vectors = [model.wv[t] for t in tokens if t in model.wv]
        if not vectors:
            return np.zeros(model.vector_size)
        return np.mean(vectors, axis=0)

    v1 = avg_vector(ref_tokens).reshape(1, -1)
    v2 = avg_vector(stu_tokens).reshape(1, -1)
    if np.all(v1 == 0) or np.all(v2 == 0):
        return 0.0

    score = cosine_similarity(v1, v2)[0][0]
    return normalize_similarity(float(score))


def sbert_similarity(reference_text, student_text):
    reference_text = safe_text(reference_text)
    student_text = safe_text(student_text)
    if not reference_text or not student_text:
        return 0.0

    model = _get_sbert_model()
    if model is None:
        return 0.0

    try:
        embeddings = model.encode([reference_text, student_text])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return normalize_similarity(float(score))
    except Exception:
        return 0.0


def aggregate_algorithm_scores(score_map):
    if not score_map:
        return 0.0

    weights = {
        "SBERT": 0.45,
        "TF-IDF": 0.25,
        "Jaccard": 0.20,
        "Word2Vec": 0.10,
    }

    total = 0.0
    total_weight = 0.0

    for algorithm, similarity in score_map.items():
        normalized = normalize_similarity(similarity)
        weight = weights.get(algorithm, 0.10)
        total += normalized * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(total / total_weight, 4)


def compute_combined_similarity(reference_text, student_text):
    reference_text = safe_text(reference_text)
    student_text = safe_text(student_text)
    if not reference_text or not student_text:
        return 0.0

    score_map = {
        "Jaccard": jaccard_similarity(reference_text, student_text),
        "TF-IDF": tfidf_similarity(reference_text, student_text),
        "Word2Vec": word2vec_similarity(reference_text, student_text),
        "SBERT": sbert_similarity(reference_text, student_text),
    }
    return aggregate_algorithm_scores(score_map)


def similarity_to_marks_and_grade(similarity, max_marks):
    normalized_similarity = normalize_similarity(similarity)
    max_marks = float(max_marks) if max_marks is not None else 0.0

    if max_marks <= 0:
        return 0.0, "F"

    marks = round(normalized_similarity * max_marks, 2)
    if normalized_similarity >= 0.80:
        grade = "A"
    elif normalized_similarity >= 0.60:
        grade = "B"
    elif normalized_similarity >= 0.40:
        grade = "C"
    elif normalized_similarity >= 0.20:
        grade = "D"
    else:
        grade = "F"
    return marks, grade