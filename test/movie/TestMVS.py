import unittest
from unittest import mock
import unittest.mock
import os

from movie.mvs import MVS
from movie.movie import Movie
from music_user.music import Music


class TestMVS(unittest.TestCase):
    @unittest.mock.patch.dict(os.environ, {
         "TMDB_API_KEY": "abc",
         "SPOTIFY_CLIENT_ID": "123",
         "SPOTIFY_CLIENT_SECRET": "456"
         }
         )
    def setUp(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True
        ):
            self.mvs = MVS()

    """Test init function."""
    def test_init_success(self):
        self.assertIsInstance(self.mvs.movie, Movie)
        self.assertIsInstance(self.mvs.music, Music)
        self.assertIsNone(self.mvs.preference)
        
    """Test return_movie_results function."""
    def test_return_movie_results(self):
        # Test default.
        results = self.mvs.return_movie_results()
        self.assertIsInstance(results, dict)
        self.assertEqual(results, {})

        # Test real return values.
        with unittest.mock.patch.object(
            Movie, "movie_search", return_value=[
                {
                    "id": 123,
                    "original_language": "language_abc",
                    "original_title": "title_abc",
                    "overview": "overview_abc",
                    "release_date": "2024",
                    "backdrop_path": "/abc/abc",
                    "poster_path": "/abc/dfg",
                    "genre_ids": "28",
                }
            ]
            ):
            results = self.mvs.return_movie_results()
            self.assertEqual(results, {
                "title_abc": {
                    "id": 123,
                    "original_language": "language_abc",
                    "original_title": "title_abc",
                    "overview": "overview_abc",
                    "release_date": "2024",
                    "backdrop_path": "/abc/abc",
                    "poster_path": "/abc/dfg",
                    "genre_ids": "28",
                }
            }
                             )

    """Test return_music_results function."""
    def test_return_music_results(self):
        # Test default.
        with unittest.mock.patch.object(
            Music, "music_search", return_value = []):
            results = self.mvs.return_music_results()
            self.assertIsInstance(results, list)
            self.assertEqual(results, [])
        
        # Test real value.
        with unittest.mock.patch.object(
            Music, "music_search", return_value = [
                {
                    "album_urls": "abc/abc",
                    "img_url": "abc/abc",
                    "name": "abc",
                    "release_date": "2024",
                    "artists": "abc"
                }
            ]
            ):
            results = self.mvs.return_music_results("abc", {})
            self.assertIsInstance(results, list)
            self.assertEqual(results, [
                {
                    "album_urls": "abc/abc",
                    "img_url": "abc/abc",
                    "name": "abc",
                    "release_date": "2024",
                    "artists": "abc"
                }
                ]
            )         

    """Test return_recom function."""
    @unittest.mock.patch.object(
            Movie, "movie_recom", return_value = ["a", "b", "c"])
    @unittest.mock.patch.object(
        Music, "music_recom", return_value = ["e", "f", "g"]
    )
    def test_return_recom(self, mock_movie_recom, mock_music_recom):
        # Test default.
        results = self.mvs.return_recom()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ["a", "b", "c"])
        self.assertEqual(results[1], ["e", "f", "g"])

        # Test movie recom.
        results = self.mvs.return_recom(
            recom_preference={"recom_type": "movie"})
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ["a", "b", "c"])
        self.assertEqual(results[1], [])

        # Test music recom.
        results = self.mvs.return_recom(
            recom_preference={"recom_type": "music"})
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], [])
        self.assertEqual(results[1], ["e", "f", "g"])       


    # def test_display_movie_details(self):
    #     pass

    # def test_display_music_details(self):
    #     pass

    # def test_start(self):
    #     pass

    # def test_decoration(self):
    #     pass

if __name__ == "__main__":
    # run with python -m unittest ./test/movie/TestMVS.py
    unittest.main()