# TestMusic.py

import unittest
from unittest.mock import patch
import os
from music_user.music import Music
from test.mock_helper import mocked_requests_get_200, mocked_requests_get_else

class TestMusic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a Music instance for all tests."""
        with patch.dict(os.environ, {"SPOTIFY_CLIENT_ID": "123", "SPOTIFY_CLIENT_SECRET": "456"}):
            cls.music = Music()

    def setUp(self):
        """Prepare test variables."""
        self.movie_name = "Harry Potter"
        self.user_preference = {"num_results": 3}
        self.recom_preference = {"num_recom": 2, "genre": "pop"}

    @patch("spotipy.Spotify.search", side_effect=mocked_requests_get_200)
    def test_music_search(self, mock_search):
        """Test the music_search function."""
        results = self.music.music_search(self.movie_name, self.user_preference)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["name"], "Test Album")

    @patch("spotipy.Spotify.search", side_effect=mocked_requests_get_else)
    def test_fetch_music(self, mock_search):
        """Test the fetch_music function."""
        result = self.music.fetch_music(self.movie_name)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result.get("albums", {}).get("items", [])), 0)

    @patch("spotipy.Spotify.search", side_effect=mocked_requests_get_200)
    def test_music_recom(self, mock_search):
        """Test the music_recom function."""
        results = self.music.music_recom(self.recom_preference)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["name"], "Test Album")

    @patch("spotipy.Spotify.search", side_effect=mocked_requests_get_200)
    def test_fetch_recommendations(self, mock_search):
        """Test the fetch_recommendations function."""
        results = self.music.fetch_recommendations(self.recom_preference)
        self.assertIsInstance(results, dict)
        self.assertGreater(len(results.get("albums", {}).get("items", [])), 0)
        self.assertEqual(results["albums"]["items"][0]["name"], "Test Album")

    def test_music_parse_response(self):
        """Test the music_parse_response function."""
        mock_response = {
            "albums": {"items": [
                {
                    "name": "Parsed Album",
                    "artists": [{"name": "Artist3"}],
                    "release_date": "2020",
                    "external_urls": {"spotify": "url3"},
                    "images": [{"url": "image3"}]
                }
            ]}
        }
        parsed = self.music.music_parse_response(mock_response, num_results=1)
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["name"], "Parsed Album")
        self.assertEqual(parsed[0]["artists"], "Artist3")

    def tearDown(self):
        """Clean up after each test."""
        self.movie_name = None
        self.user_preference = None
        self.recom_preference = None

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        del cls.music

# if __name__ == "__main__":
#     unittest.main(argv=[''], verbosity=2, exit=False)