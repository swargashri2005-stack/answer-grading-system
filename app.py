import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import Error as MySQLError
from db import execute_query, fetch_one, fetch_all
from grading_service import grade_question


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)

# Required for Flask flash messages
# Later, move this secret key to a .env file
app.secret_key = os.getenv("SECRET_KEY")


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------------------------------
# DATABASE DASHBOARD
# --------------------------------------------------

@app.route("/database")
def database_dashboard():
    # Authentication is not currently implemented; add an admin guard here
    # if authentication is introduced in the future.
    try:
        students = fetch_all(
            """
            SELECT id, roll_number, name, category, created_at
            FROM students
            ORDER BY created_at DESC
            """
        )
        questions = fetch_all(
            """
            SELECT id, question_text, max_marks, created_at
            FROM questions
            ORDER BY created_at DESC
            """
        )
        answers = fetch_all(
            """
            SELECT id, question_id, student_id, answer_type, answer_text,
                   marks_obtained, created_at
            FROM answers
            ORDER BY created_at DESC
            """
        )
        results = fetch_all(
            """
            SELECT *
            FROM results
            ORDER BY created_at DESC
            """
        )
    except MySQLError:
        app.logger.exception("Could not load the database dashboard")
        return render_template("database_unavailable.html"), 503

    return render_template(
        "database.html",
        students=students,
        questions=questions,
        answers=answers,
        results=results,
        last_updated=datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
    )


# --------------------------------------------------
# ADD QUESTION
# --------------------------------------------------

@app.route("/add_question", methods=["GET", "POST"])
def add_question():

    # If the form is submitted
    if request.method == "POST":

        # Get data from HTML form
        question_text = request.form["question_text"]
        max_marks = request.form["max_marks"]

        # Insert question into MySQL
        execute_query(
            """
            INSERT INTO questions (question_text, max_marks)
            VALUES (%s, %s)
            """,
            (question_text, max_marks)
        )

        # Show success message
        flash("Question added successfully!")

        # Redirect back to Add Question page
        return redirect(url_for("add_question"))

    # If GET request, show the form
    return render_template("add_question.html")


# --------------------------------------------------
# ADD STUDENT
# --------------------------------------------------

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    # If the form is submitted
    if request.method == "POST":

        # Get data from HTML form
        roll_number = request.form["roll_number"]
        name = request.form["name"]
        category = request.form.get("category")

        # Check whether roll number already exists
        existing = fetch_one(
            """
            SELECT id
            FROM students
            WHERE roll_number = %s
            """,
            (roll_number,)
        )

        # If student already exists
        if existing:
            flash("Error: Roll number already exists.")
            return redirect(url_for("add_student"))

        # Insert new student
        execute_query(
            """
            INSERT INTO students (roll_number, name, category)
            VALUES (%s, %s, %s)
            """,
            (roll_number, name, category)
        )

        # Show success message
        flash("Student added successfully!")

        # Redirect back to Add Student page
        return redirect(url_for("add_student"))

    # If GET request, show the form
    return render_template("add_student.html")


# --------------------------------------------------
# ADD REFERENCE ANSWER
# --------------------------------------------------

@app.route("/add_reference_answer", methods=["GET", "POST"])
def add_reference_answer():

    # If the form is submitted
    if request.method == "POST":

        # Get data from HTML form
        question_id = request.form["question_id"]
        answer_text = request.form["answer_text"]

        # Insert reference answer
        #
        # student_id = None
        # means NULL in MySQL because this is a reference answer,
        # not a student's answer.
        try:
            execute_query(
                """
                INSERT INTO answers
                (question_id, student_id, answer_type, answer_text)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    question_id,
                    None,
                    "reference",
                    answer_text
                )
            )
        except MySQLError:
            app.logger.exception("Could not save the reference answer")
            return render_template("database_unavailable.html"), 503

        # Show success message
        flash("Reference answer added successfully!")

        # Redirect back to the same page
        return redirect(url_for("add_reference_answer"))

    # Get all questions for the dropdown
    try:
        questions = fetch_all(
            """
            SELECT id, question_text
            FROM questions
            """
        )
    except MySQLError:
        app.logger.exception("Could not load questions for reference answers")
        return render_template("database_unavailable.html"), 503

    # Send questions to HTML template
    return render_template(
        "add_reference_answer.html",
        questions=questions
    )


# --------------------------------------------------
# ADD STUDENT ANSWER
# --------------------------------------------------

@app.route("/add_student_answer", methods=["GET", "POST"])
def add_student_answer():

    # If the form is submitted
    if request.method == "POST":

        # Get question and student from form
        question_id = request.form["question_id"]
        student_id = request.form["student_id"]

        # Get answer text
        #
        # If answer_text does not exist, use ""
        # strip() removes spaces from beginning/end.
        answer_text = request.form.get("answer_text", "").strip()

        # If answer is empty,
        # store None so MySQL stores NULL.
        answer_text = answer_text if answer_text else None

        # Insert student answer
        try:
            execute_query(
                """
                INSERT INTO answers
                (question_id, student_id, answer_type, answer_text)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    question_id,
                    student_id,
                    "student",
                    answer_text
                )
            )
        except MySQLError:
            app.logger.exception("Could not save the student answer")
            return render_template("database_unavailable.html"), 503

        # Show success message
        flash("Student answer added successfully!")

        # Redirect back to the same page
        return redirect(url_for("add_student_answer"))

    # Get all questions for dropdown
    try:
        questions = fetch_all(
            """
            SELECT id, question_text
            FROM questions
            """
        )

        # Get all students for dropdown
        students = fetch_all(
            """
            SELECT id, roll_number, name
            FROM students
            """
        )
    except MySQLError:
        app.logger.exception("Could not load data for student answers")
        return render_template("database_unavailable.html"), 503

    # Send both lists to HTML
    return render_template(
        "add_student_answer.html",
        questions=questions,
        students=students
    )


# --------------------------------------------------
# GRADE ANSWERS
# --------------------------------------------------

@app.route("/grade_answers", methods=["GET", "POST"])
def grade_answers():

    # If teacher submits the grading form
    if request.method == "POST":

        # Get selected question ID
        question_id = request.form["question_id"]

        try:

            # Start grading process
            grade_question(question_id)

            # If grading succeeds
            flash("Grading complete!")

        except ValueError as e:

            # If grading fails because of a validation problem
            flash(f"Grading failed: {e}")

        except MySQLError:
            app.logger.exception("Could not grade answers")
            return render_template("database_unavailable.html"), 503

        # Show results page
        return redirect(
            url_for(
                "grade_results",
                question_id=question_id
            )
        )

    # For GET request,
    # get all questions for dropdown.
    try:
        questions = fetch_all(
            """
            SELECT id, question_text
            FROM questions
            """
        )
    except MySQLError:
        app.logger.exception("Could not load questions for grading")
        return render_template("database_unavailable.html"), 503

    # Show grading page
    return render_template(
        "grade_answers.html",
        questions=questions
    )


# --------------------------------------------------
# GRADE RESULTS
# --------------------------------------------------

@app.route("/grade_results/<int:question_id>")
def grade_results(question_id):

    # Get grading results from MySQL
    #
    # JOIN students so that we can display
    # student's roll number and name.
    try:
        results = fetch_all(
            """
            SELECT
                r.*,
                s.roll_number,
                s.name
            FROM results r
            JOIN students s
                ON r.student_id = s.id
            WHERE r.question_id = %s
            ORDER BY s.name, r.algorithm
            """,
            (question_id,)
        )
    except MySQLError:
        app.logger.exception("Could not load grading results")
        return render_template("database_unavailable.html"), 503

    # Send results to HTML
    return render_template(
        "grade_results.html",
        results=results
    )


# --------------------------------------------------
# START FLASK SERVER
# --------------------------------------------------

# IMPORTANT:
# This must remain at the VERY BOTTOM of the file.

if __name__ == "__main__":
    app.run(debug=False)