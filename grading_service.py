from db import fetch_one, fetch_all, execute_query
from grading import (
    compute_combined_similarity,
    jaccard_similarity,
    sbert_similarity,
    similarity_to_marks_and_grade,
    tfidf_similarity,
    word2vec_similarity,
)


def save_result(question_id, student_id, algorithm, similarity_score, marks, letter_grade):
    execute_query(
        """INSERT INTO results (question_id, student_id, algorithm, similarity_score, marks, letter_grade)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (question_id, student_id, algorithm, similarity_score, marks, letter_grade)
    )


def grade_question(question_id):
    question = fetch_one("SELECT * FROM questions WHERE id = %s", (question_id,))
    if not question:
        raise ValueError("Question not found")

    reference = fetch_one(
        "SELECT * FROM answers WHERE question_id = %s AND answer_type = 'reference'",
        (question_id,)
    )
    if not reference or not reference["answer_text"]:
        raise ValueError("No reference answer set for this question")

    reference_text = reference["answer_text"]
    max_marks = question["max_marks"]

    student_answers = fetch_all(
        "SELECT * FROM answers WHERE question_id = %s AND answer_type = 'student'",
        (question_id,)
    )

    execute_query("DELETE FROM results WHERE question_id = %s", (question_id,))

    for ans in student_answers:
        student_id = ans["student_id"]
        student_text = ans["answer_text"]

        if not student_text or not str(student_text).strip():
            continue

        algorithms = {
            "Jaccard": jaccard_similarity(reference_text, student_text),
            "TF-IDF": tfidf_similarity(reference_text, student_text),
            "Word2Vec": word2vec_similarity(reference_text, student_text),
            "SBERT": sbert_similarity(reference_text, student_text),
        }

        for algo_name, similarity in algorithms.items():
            marks, grade = similarity_to_marks_and_grade(similarity, max_marks)
            save_result(question_id, student_id, algo_name, similarity, marks, grade)

        overall_similarity = compute_combined_similarity(reference_text, student_text)
        overall_marks, overall_grade = similarity_to_marks_and_grade(overall_similarity, max_marks)
        save_result(question_id, student_id, "Overall", overall_similarity, overall_marks, overall_grade)

    return True