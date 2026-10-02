import math
import unittest

from grading import normalize_similarity, similarity_to_marks_and_grade


class GradingValidationTests(unittest.TestCase):
    def test_none_and_nan_are_treated_as_zero(self):
        self.assertEqual(normalize_similarity(None), 0.0)
        self.assertEqual(normalize_similarity(float('nan')), 0.0)

    def test_similarity_is_clamped_to_valid_range(self):
        self.assertEqual(normalize_similarity(1.5), 1.0)
        self.assertEqual(normalize_similarity(-0.2), 0.0)

    def test_marks_and_grade_are_safe(self):
        marks, grade = similarity_to_marks_and_grade(1.3, 10)
        self.assertEqual(marks, 10.0)
        self.assertEqual(grade, 'A')


if __name__ == '__main__':
    unittest.main()
