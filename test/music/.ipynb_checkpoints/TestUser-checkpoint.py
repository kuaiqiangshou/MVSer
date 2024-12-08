# TestUser.py

import unittest
from unittest.mock import patch
import os
from music_user.user import User

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a User instance for all tests."""
        cls.user = User()

    def setUp(self):
        """Prepare test variables."""
        self.valid_preferences = {
            "num_results": 3,
            "is_recom": {"recom_type": "Music", "num_recom": 2, "genre": "pop"}
        }
        self.invalid_preferences = {
            "num_results": -1,
            "is_recom": {"recom_type": "InvalidType", "num_recom": -2, "genre": None}
        }

    def test_default_preferences(self):
        """Test the default user preferences."""
        self.assertEqual(self.user.movie_name, "Harry Potter")
        self.assertEqual(self.user.preference["num_results"], 3)
        self.assertEqual(self.user.preference["is_recom"]["genre"], "pop")

    def test_check_inputs_valid(self):
        """Test valid user preferences."""
        self.user.check_inputs(self.valid_preferences)
        self.assertEqual(self.valid_preferences["num_results"], 3)
        self.assertEqual(self.valid_preferences["is_recom"]["recom_type"], "Music")
        self.assertGreater(self.valid_preferences["is_recom"]["num_recom"], 0)

    def test_check_inputs_invalid(self):
        """Test invalid user preferences."""
        with self.assertRaises(ValueError):
            self.user.check_inputs(self.invalid_preferences)

    @patch("builtins.print")
    def test_display_preference(self, mock_print):
        """Test the display_preference method."""
        self.user.display_preference()
        expected_calls = [
            ("Movie Name:", "Harry Potter"),
            ("User Preferences:",),
        ]
        expected_calls.extend((f"{key}: {value}",) for key, value in self.user.preference.items())
        for call in expected_calls:
            mock_print.assert_any_call(*call)

    def tearDown(self):
        """Clean up variables after each test."""
        self.valid_preferences = None
        self.invalid_preferences = None

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        del cls.user

# if __name__ == "__main__":
#     unittest.main(argv=[''], verbosity=2, exit=False)