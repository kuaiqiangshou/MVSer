import unittest
from unittest import mock
import unittest.mock
from unittest.mock import call
import os

from movie.mvs import MVS
from movie.movie import Movie
from music_user.music import Music
from music_user.user import User


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
        self.assertIsInstance(self.mvs.user, User)
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


    """Test display_movie_details function."""
    @unittest.mock.patch("builtins.print", clear=True)
    @unittest.mock.patch("movie.mvs.PRINT_MOOD", new="simple")
    def test_display_movie_details(self, mock_print):
        # Test default.
        self.assertIsNone(self.mvs.display_movie_details())
        mock_print.assert_called_with("Sorry, there is nothing to display :(")

        # Test real value.
        movie_info = {
            "id": "123",
            "original_language": "language_abc",
            "original_title": "title_abc",
            "overview": "overview_abc",
            "release_date": "2024",
            "backdrop_path": "/abc/abc",
            "backdrop_url": "https://image.tmdb.org/t/p/w500/abc/abc",
            "poster_path": "/abc/dfg",
            "poster_url": "https://image.tmdb.org/t/p/w500/abc/dfg",
            "genre_ids": ["28"],
            "genre_names": ["Action"],
            "collection": "abc",
            "collection_poster_path": "/collect/abc",
            "collection_poster_url": "https://image.tmdb.org/t/p/w500/collect/abc",
            "homepage": "homepage"
        }
        with unittest.mock.patch.object(
            MVS, "display_poster", return_value=None
            ):
            self.mvs.display_movie_details(movie_info)
            mock_print.assert_has_calls(
                [
                    call("** title_abc **\n"),
                    call("Overview: overview_abc"),
                    call("Homepage: homepage"),
                    call("Release Date: 2024"),
                    call("Genre: [\'Action\']"),
                    call("Belongs to collection: abc"),
                    call()
                ]
            )

    """Test display_music_details function"""
    @unittest.mock.patch("builtins.print", clear=True)
    @unittest.mock.patch("movie.mvs.PRINT_MOOD", new="simple")
    def test_display_music_details(self, mock_print):
        # Test default.
        self.assertIsNone(self.mvs.display_music_details())
        mock_print.assert_called_with("Sorry, there is nothing to display :(")

        # Test real value.
        music_info = {
            "name": "abc",
            "img_url": "abc",
            "album_urls": "abc/abc",
            "artists": "abc",
            "release_date": 2024,
        }
        with unittest.mock.patch.object(
            MVS, "display_poster", return_value=None
            ):
            self.mvs.display_music_details(music_info)
            mock_print.assert_has_calls(
                [
                    call("** abc **\n"),
                    call("Album: abc/abc"),
                    call("Artists: abc"),
                    call("Release Date: 2024"),
                    call()
                ]
            )

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("movie.mvs.MVS.decoration")
    @unittest.mock.patch("music_user.user.User")
    def test_start(self, mock_input, mock_decoration, mock_user):
        mock_user.return_value.preference = {
            "num_results": 3,
            "music_version": "clean",
            "movie_genre": None,
            "music_genre": None,
            "is_recom": {
                "recom_type": "Both", 
                "num_recom": 3,
                "genre": "pop"
            }
        }
        mock_user.return_value.user_input.return_value = None
        mock_user.return_value.movie_name = "abc"
        
        with unittest.mock.patch.object(MVS, "return_movie_results"
            ) as mock_return_movie_results:
            with unittest.mock.patch.object(
                MVS, "display_movie_details"
            ):
                # With empty movie results.
                mock_return_movie_results.return_value = {}
                self.mvs.start()
                mock_decoration.assert_any_call(
                    emo=":loudly_crying_face:",
                    info="Sorry, there is no matched movie!"
                )
                with self.assertRaises(AssertionError):
                    mock_decoration.assert_any_call(
                        emo=":movie_camera:",
                        info="Movie Details for abc"   
                    )
                with self.assertRaises(AssertionError):
                    mock_decoration.assert_any_call(
                        emo=":musical_notes:",
                        info="Music Album in abc"
                    )

                # With non-empty movie results.
                mock_decoration.reset_mock()
                mock_return_movie_results.return_value = {"abc": 123}
                self.mvs.start()
                with self.assertRaises(AssertionError):
                    mock_decoration.assert_any_call(
                        emo=":loudly_crying_face:",
                        info="Sorry, there is no matched movie!"
                    )
                mock_decoration.assert_any_call(
                    emo=":movie_camera:",
                    info="Movie Details for abc"   
                )
                mock_decoration.assert_any_call(
                    emo=":musical_notes:",
                    info="Music Album in abc"
                )


    """Test decoration function."""
    @unittest.mock.patch("builtins.print")
    @unittest.mock.patch("movie.mvs.PRINT_MOOD", new="simple")
    def test_decoration(self, mock_print):
        # Test default.
        self.mvs.decoration()
        mock_print.assert_called_with("******** info ********\n")

        # Test different mode.
        self.mvs.decoration(mode="title")
        mock_print.assert_called_with("** info **\n")

        self.mvs.decoration(mode="other")
        mock_print.assert_called_with("******** info ********\n")

        # Test maximum length.
        self.mvs.decoration(info="aaaaaaaaaaaaaaaaaaaaa", mode="other")
        nb_star = 18
        mock_print.assert_called_with(
            f"{'**' * nb_star} aaaaaaaaaaaaaaaaaaaaa {'**' * nb_star}\n")
      
        
if __name__ == "__main__":
    # run with python -m unittest ./test/movie/TestMVS.py
    unittest.main(argv =[''], verbosity=2, exit=False)