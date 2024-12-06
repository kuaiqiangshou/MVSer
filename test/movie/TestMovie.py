import unittest
import os
from unittest import mock
import unittest.mock

from movie.movie import Movie
from movie.exceptions import APICallError
from test.helper import *
    
class TestMovie(unittest.TestCase):   

    @unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
    def setUp(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True
            ):
                self.movie = Movie()
        
    
    """Test init function."""
    def test_init_true(self):
        self.assertEqual(self.movie.get_TMDB_key, "abc")

        self.assertIsNotNone(self.movie.config)
        self.assertEqual(
            self.movie.config["basic_url"], "https://api.themoviedb.org/3"
            )
        self.assertEqual(self.movie.config["search_endpoint"], "/search/movie")
        self.assertEqual(
            self.movie.config["collection_endpoint"],
            "/movie/MOVIE_ID?language=en-US&page=1"
            )
        self.assertEqual(
            self.movie.config["recommendation_endpoint"],
            "/trending/movie/day?language=en-US"
            )
        self.assertEqual(self.movie.url, "https://api.themoviedb.org/3")

        self.assertDictEqual(
            self.movie.header, 
            {
                "accept": "application/json",
                "Authorization": "Bearer " + "abc"
                }
            )
        
    def test_init_fail(self):
        # Test if no TMDB_API_Key setup at all.
        names_to_remove = {"TMDB_API_KEY"}
        modified_environ = {
            k: v for k, v in os.environ.items() if k not in names_to_remove
        }
        with mock.patch.dict(os.environ, modified_environ, clear=True):
            with self.assertRaises(ValueError):
                movie = Movie()
                self.assertEqual(movie.get_TMDB_key, None)

        # After setup API key proporly, but get API connection error.
        with unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"}):
            with unittest.mock.patch.object(
                Movie, "test_api_connection", return_value=False):
                with self.assertRaises(ConnectionError):
                    Movie()

    """Test movie_search function."""
    @unittest.mock.patch.object(Movie, "fetch_movie", return_value = {})
    @unittest.mock.patch.object(
        Movie, "movie_parse_response", return_value = ["a", "b"]
        )
    def test_movie_search(
        self, mock_fetch_movie, mock_movie_parse_response, 
        ):
        self.movie.movie_search(None, {})
        self.assertEqual(self.movie.movie_search("abc", {}), ["a", "b"])
        
        self.movie.movie_search("abc", {})
        self.assertEqual(self.movie.movie_search("abc", {}), ["a", "b"])


    """Test fetch_movie function."""
    def test_fetch_movie_success(self):

        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            movie_name = "harry potter"
            response = self.movie.fetch_movie(movie_name=movie_name)
            self.assertEqual(
                self.movie.search_query,
                "https://api.themoviedb.org/3/search/movie?query=harry%20"\
                    "potter&language=en-US&page=1"
                )

            self.assertIsInstance(response, dict)

    def test_fetch_movie_fails(self):
        # Other status_code. 
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_else
            ):
            response = self.movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_request_exception
            ):
            response = self.movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)
 
        # Other error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_exception
            ):
            response = self.movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)  

    """Test fetch_collection function."""
    def test_fetch_collection_success(self):
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            response = self.movie.fetch_collection(id="123")
            self.assertEqual(
                self.movie.collection_query,
                "https://api.themoviedb.org/3/movie/123?language=en-US&page=1"
                )

            self.assertIsInstance(response, dict)

    def test_fetch_collection_fails(self):
        # empty input.
        response = self.movie.fetch_collection(id="")
        self.assertEqual(response, None)

        # Other status_code. 
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_else
            ):
            response = self.movie.fetch_collection(id="123")
            self.assertEqual(response, None)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_resquests_get_request_exception
            ):
            response = self.movie.fetch_collection(id="1234")
            self.assertEqual(response, None)
        
        # Other error.
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_resquests_get_exception
            ):
            response = self.movie.fetch_collection(id="123")
            self.assertEqual(response, None) 

    # """Test movie_parse_response function."""
    # def test_movie_parse_response_empty(self, mock_test_api_connection):
    #     movie = Movie()


    # def test_movie_recom(self):
    #     pass

    # def test_fetch_recom(self):
    #     pass

    # def test_test_api_connection(self):
    #     pass


if __name__ == "__main__":
    unittest.main()