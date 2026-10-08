import unittest
from unittest.mock import patch

from mysql.connector import Error as MySQLError

import app


class DatabaseDashboardTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    @patch("app.fetch_all")
    def test_displays_tables_counts_timestamp_and_actual_result_columns(self, fetch_all):
        fetch_all.side_effect = [
            [
                {
                    "id": 7,
                    "roll_number": "R-7",
                    "name": "A Student",
                    "category": "A",
                    "created_at": "2026-01-01",
                }
            ],
            [
                {
                    "id": 8,
                    "question_text": "Question text",
                    "max_marks": 10,
                    "created_at": "2026-01-02",
                }
            ],
            [
                {
                    "id": 9,
                    "question_id": 8,
                    "student_id": 7,
                    "answer_type": "student",
                    "answer_text": "Student response",
                    "marks_obtained": None,
                    "created_at": "2026-01-03",
                }
            ],
            [{"custom_result_field": "dynamic value"}],
        ]

        response = self.client.get("/database")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Total Students", response.data)
        self.assertIn(b"Total Questions", response.data)
        self.assertIn(b"Total Answers", response.data)
        self.assertIn(b"Total Results", response.data)
        self.assertIn(b"Last Updated:", response.data)
        self.assertIn(b"Custom Result Field", response.data)
        self.assertIn(b"dynamic value", response.data)
        self.assertIn(b"Student response", response.data)
        self.assertIn(b"Refresh Database", response.data)
        self.assertEqual(fetch_all.call_count, 4)
        for query_call in fetch_all.call_args_list:
            self.assertIn("ORDER BY created_at DESC", query_call.args[0])
            self.assertTrue(query_call.args[0].lstrip().startswith("SELECT"))

    @patch("app.fetch_all", return_value=[])
    def test_shows_empty_states_for_all_tables(self, fetch_all):
        response = self.client.get("/database")

        self.assertEqual(response.status_code, 200)
        for message in (
            "No students found.",
            "No questions found.",
            "No answers found.",
            "No results found.",
        ):
            self.assertIn(message.encode(), response.data)
        self.assertEqual(fetch_all.call_count, 4)

    @patch("app.fetch_all", side_effect=MySQLError("database unavailable"))
    def test_database_error_uses_existing_unavailable_page(self, fetch_all):
        response = self.client.get("/database")

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Database unavailable", response.data)
        fetch_all.assert_called_once()


if __name__ == "__main__":
    unittest.main()
