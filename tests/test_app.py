import unittest
from unittest.mock import patch

from mysql.connector import Error as MySQLError

import app


class AddReferenceAnswerDatabaseFailureTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    @patch("app.fetch_all", side_effect=MySQLError("database unavailable"))
    def test_get_returns_service_unavailable_page(self, _fetch_all):
        response = self.client.get("/add_reference_answer")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)
        self.assertIn(b"DB_HOST", response.data)

    @patch("app.execute_query", side_effect=MySQLError("database unavailable"))
    def test_post_does_not_report_success_when_database_is_unavailable(
        self, _execute_query
    ):
        response = self.client.post(
            "/add_reference_answer",
            data={"question_id": "1", "answer_text": "Reference answer"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)
        self.assertNotIn(b"Reference answer added successfully", response.data)


class AddStudentAnswerDatabaseFailureTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    @patch("app.fetch_all", side_effect=MySQLError("database unavailable"))
    def test_get_returns_service_unavailable_page(self, _fetch_all):
        response = self.client.get("/add_student_answer")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)

    @patch("app.execute_query", side_effect=MySQLError("database unavailable"))
    def test_post_does_not_report_success_when_database_is_unavailable(
        self, _execute_query
    ):
        response = self.client.post(
            "/add_student_answer",
            data={
                "question_id": "1",
                "student_id": "1",
                "answer_text": "Student answer",
            },
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)
        self.assertNotIn(b"Student answer added successfully", response.data)


class GradeAnswersDatabaseFailureTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    @patch("app.fetch_all", side_effect=MySQLError("database unavailable"))
    def test_get_returns_service_unavailable_page(self, _fetch_all):
        response = self.client.get("/grade_answers")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)

    @patch("app.grade_question", side_effect=MySQLError("database unavailable"))
    def test_post_returns_service_unavailable_when_grading_cannot_access_database(
        self, _grade_question
    ):
        response = self.client.post(
            "/grade_answers",
            data={"question_id": "1"},
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)


class GradeResultsDatabaseFailureTests(unittest.TestCase):
    @patch("app.fetch_all", side_effect=MySQLError("database unavailable"))
    def test_get_returns_service_unavailable_page(self, _fetch_all):
        response = app.app.test_client().get("/grade_results/1")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)


if __name__ == "__main__":
    unittest.main()
