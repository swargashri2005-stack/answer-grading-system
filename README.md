# NLP-Based Answer Grading System

An NLP-based web application for automatically evaluating student answers against a reference answer. The system uses Natural Language Processing techniques to compare answers and generate a similarity-based score.

## 📌 Project Overview

Manual answer evaluation can be time-consuming and may vary from one evaluator to another. This project provides a web-based system that helps automate the initial evaluation of descriptive answers.

The application allows users to:

- Add student information
- Add questions
- Add reference/model answers
- Add student answers
- Grade student answers automatically
- View grading results
- View a read-only dashboard of students, questions, answers, and results
- Store and retrieve data using MySQL

## 🎯 Objectives

1. Automate the initial evaluation of descriptive answers.
2. Compare student answers with reference answers using NLP.
3. Calculate semantic/content similarity using text-based features.
4. Reduce manual effort in answer evaluation.
5. Provide a simple web interface for managing students, questions, answers, and results.

## 🛠️ Technologies Used

- **Python**
- **Flask** – Web application framework
- **HTML** – Web page structure
- **CSS** – Styling and layout
- **JavaScript** – Client-side interaction
- **MySQL** – Database
- **NLTK / NLP preprocessing** – Text preprocessing
- **Scikit-learn** – TF-IDF and similarity calculation
- **Git/GitHub** – Version control (if used)

## 🧠 Grading Method

The core grading workflow is based on comparing the student's answer with a reference answer.

### Basic workflow

```text
Reference Answer
       │
       ▼
Text Preprocessing
       │
       ▼
TF-IDF Vectorization
       │
       ▼
Reference Vector
       │
       │
       │ Cosine Similarity
       │
       ▼
Student Answer
       │
       ▼
Text Preprocessing
       │
       ▼
TF-IDF Vectorization
       │
       ▼
Student Vector
       │
       ▼
Similarity Score
       │
       ▼
Final Grade / Marks
```

A higher similarity score indicates greater textual/content similarity between the student answer and the reference answer. The final conversion from similarity to marks depends on the grading logic implemented in the project.

## 📂 Project Structure

```text
Answer-Grading-System/
│
├── venv/
│   └── Python virtual environment
│
├── static/
│   ├── css/
│   └── js/
│       └── script.js
│
├── templates/
│   ├── about.html
│   ├── add_question.html
│   ├── add_reference_answer.html
│   ├── add_student_answer.html
│   ├── add_student.html
│   ├── base.html
│   ├── grade_answers.html
│   ├── grade_results.html
│   └── home.html
│
├── tests/
│   ├── __init__.py
│   └── test_grading.py
│
├── app.py
├── db.py
├── grading.py
├── grading_service.py
├── mysql_search.txt
├── requirements.txt
└── schema.sql
```

### Important Files

| File/Folder | Purpose |
|---|---|
| `app.py` | Main Flask application and URL routes |
| `db.py` | Database connection and database operations |
| `grading.py` | Core NLP/grading calculations |
| `grading_service.py` | Coordinates the grading workflow |
| `templates/` | HTML pages used by Flask |
| `static/` | CSS and JavaScript files |
| `schema.sql` | SQL commands for creating the database structure |
| `requirements.txt` | Python dependencies |
| `tests/` | Testing files |
| `test_grading.py` | Tests grading functionality |
| `venv/` | Isolated Python environment |

## 🔄 Application Flow

```text
User
  │
  ▼
Browser
  │
  ▼
Flask Routes (app.py)
  │
  ├───────────────┐
  ▼               ▼
Templates       Backend Services
                  │
          ┌───────┴────────┐
          ▼                ▼
       db.py        grading_service.py
          │                │
          ▼                ▼
        MySQL          grading.py
                           │
                           ▼
                       NLP/TF-IDF
                           │
                           ▼
                    Similarity Score
                           │
                           ▼
                     Grading Result
                           │
                           ▼
                       MySQL
                           │
                           ▼
                  grade_results.html
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Answer-Grading-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

1. Install and start MySQL.
2. Create the required database.
3. Run the SQL commands in:

```text
schema.sql
```

4. Update the database configuration in `db.py` or your project's configuration file according to your local MySQL username, password, host, and database name.

Example configuration:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "answer_grading"
```

Do not commit real passwords or other secrets to GitHub.

## ▶️ Running the Application

Activate the virtual environment and run:

```bash
python app.py
```

Then open the URL shown by Flask, commonly:

```text
http://127.0.0.1:5000/
```

or

```text
http://localhost:5000/
```

## 📝 Typical Usage

1. Open the home page.
2. Add a student.
3. Add a question.
4. Add the reference/model answer.
5. Add the student's answer.
6. Open the grading page.
7. Run the grading process.
8. View the calculated score and result.

## 🗄️ Database Dashboard

Open **Database Updates** in the navigation or visit `/database` to review the
current students, questions, answers, and results stored in MySQL. The page is
read-only; use **Refresh Database** to reload the latest records. No
authentication system currently exists in the application, so this dashboard
is not access-controlled and should only be exposed to trusted users.

## 🧪 Testing

The project contains a `tests` directory for testing.

Run the grading tests according to the test framework used in the project. For example, if `pytest` is included in your dependencies:

```bash
pytest
```

## 🔐 Security Notes

- Do not upload database passwords to GitHub.
- Do not commit `.env` files containing secrets.
- Use environment variables for sensitive configuration.
- Do not upload the `venv/` folder to GitHub.

A typical `.gitignore` should include:

```text
venv/
__pycache__/
*.pyc
.env
```

## 📈 Future Improvements

Possible future improvements include:

- Semantic similarity using transformer/SBERT models
- BERTScore-based evaluation
- ROUGE-based evaluation
- Better handling of synonyms and paraphrased answers
- Keyword and concept-based scoring
- Teacher/admin authentication
- Student result history
- Improved grading calibration
- Dashboard and analytics
- REST API integration
- More comprehensive automated tests

## ⚠️ Limitations

TF-IDF and cosine similarity primarily measure similarity based on the words/features present in the texts. Therefore, two answers with the same meaning but substantially different wording may not always receive a high similarity score.

The system should therefore be treated as an automated assistance tool rather than a complete replacement for human academic evaluation.

## 👩‍💻 Project Type

**Academic / Educational NLP Project**

**Project:** NLP-Based Automatic Answer Grading System

**Primary Area:** Natural Language Processing (NLP), Machine Learning, Web Development, and Database Management

## 📄 License

This project is intended for academic and educational use. Add an appropriate open-source license if you plan to distribute the project publicly.




### sql command to access database
CMD
 ↓
mysql -u root -p
 ↓
SHOW DATABASES;
 ↓
USE answer_grading;
 ↓
SHOW TABLES;
 ↓
SELECT * FROM results;