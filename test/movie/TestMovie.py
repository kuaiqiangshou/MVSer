import unittest
import os
from unittest import mock
import unittest.mock

from movie.movie import Movie
from movie.exceptions import APICallError
from test.helper import *
    
@unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
class TestMovie(unittest.TestCase):   

    """Test init function."""
    def test_init_true(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        self.assertEqual(os.environ["TMDB_API_KEY"], "abc")
        self.assertEqual(movie.get_TMDB_key, "abc")

        self.assertIsNotNone(movie.config)
        self.assertEqual(
            movie.config["basic_url"], "https://api.themoviedb.org/3"
            )
        self.assertEqual(movie.config["search_endpoint"], "/search/movie")
        self.assertEqual(
            movie.config["collection_endpoint"],
            "/movie/MOVIE_ID?language=en-US&page=1"
            )
        self.assertEqual(
            movie.config["recommendation_endpoint"],
            "/trending/movie/day?language=en-US"
            )
        self.assertEqual(movie.url, "https://api.themoviedb.org/3")

        self.assertDictEqual(
            movie.header, 
            {
                "accept": "application/json",
                "Authorization": "Bearer " + "abc"
                }
            )
        
    def test_init_false(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=False):
            with self.assertRaises(ConnectionError):
                Movie()

    """Test movie_search function."""
    @unittest.mock.patch.object(Movie, "fetch_movie", return_value = {})
    @unittest.mock.patch.object(
        Movie, "movie_parse_response", return_value = ["a", "b"]
        )
    def test_movie_search(self, mock_fetch_movie, mock_movie_parse_response):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        movie.movie_search(None, {})
        self.assertEqual(movie.movie_search("abc", {}), ["a", "b"])
        
        movie.movie_search("abc", {})
        self.assertEqual(movie.movie_search("abc", {}), ["a", "b"])


    """Test fetch_movie function."""
    def test_fetch_movie_success(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            movie_name = "harry potter"
            response = movie.fetch_movie(movie_name=movie_name)
            self.assertEqual(
                movie.search_query,
                "https://api.themoviedb.org/3/search/movie?query=harry%20potter&"\
                    "language=en-US&page=1"
                )

            self.assertIsInstance(response, dict)

    def test_fetch_movie_fails(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        # Other status_code. 
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_else
            ):
            response = movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_request_exception
            ):
            response = movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)
 
        # Other error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_exception
            ):
            response = movie.fetch_movie(movie_name="abc")
            self.assertEqual(response, None)  

    """Test fetch_collection function."""
    def test_fetch_collection_success(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            response = movie.fetch_collection(id="123")
            self.assertEqual(
                movie.collection_query,
                "https://api.themoviedb.org/3/movie/123?language=en-US&page=1"
                )

            self.assertIsInstance(response, dict)

    def test_fetch_collection_fails(self):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        # empty input.
        response = movie.fetch_collection(id="")
        self.assertEqual(response, None)

        # Other status_code. 
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_else
            ):
            response = movie.fetch_collection(id="123")
            self.assertEqual(response, None)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_resquests_get_request_exception
            ):
            response = movie.fetch_collection(id="1234")
            self.assertEqual(response, None)
        
        # Other error.
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_resquests_get_exception
            ):
            response = movie.fetch_collection(id="123")
            self.assertEqual(response, None) 


    # @unittest.mock.patch("requests.get", side_effect=mocked_requests_get_else)
    # def test_fetch_collection_else(self, mock_get):
    #     with unittest.mock.patch.object(
    #         Movie, "test_api_connection", return_value=True):
    #         movie = Movie()

    #     response = movie.fetch_collection(id="")
    #     self.assertEqual(response, None)

    # @unittest.mock.patch(
    #         "requests.get",
    #         side_effect=mocked_resquests_get_request_exception
    #         )
    # def test_fetch_collection_request_exception(self, mock_get):
    #     with unittest.mock.patch.object(
    #         Movie, "test_api_connection", return_value=True):
    #         movie = Movie()

    #     movie_name = "abc"
    #     response = movie.fetch_movie(movie_name=movie_name)
    #     self.assertEqual(response, None)    

    # @unittest.mock.patch(
    #         "requests.get",
    #         side_effect=mocked_resquests_get_exception
    #         )
    # def test_fetch_collection_exception(self, mock_get):
    #     with unittest.mock.patch.object(
    #         Movie, "test_api_connection", return_value=True):
    #         movie = Movie()

    #     movie_name = "abc"
    #     response = movie.fetch_movie(movie_name=movie_name)
    #     self.assertEqual(response, None) 
        

    # def test_movie_parse_response(self):
    #     pass

    # def test_movie_recom(self):
    #     pass

    # def test_fetch_recom(self):
    #     pass

    # def test_test_api_connection(self):
    #     pass


if __name__ == "__main__":
    unittest.main()