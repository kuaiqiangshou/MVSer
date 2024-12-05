import unittest
import os
from unittest import mock
import unittest.mock

from movie.movie import Movie

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
            
@unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
class TestMovie(unittest.TestCase):   

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

    @unittest.mock.patch.object(Movie, "fetch_movie", return_value = {})
    @unittest.mock.patch.object(
        Movie, "movie_parse_response", return_value = ["a", "b"]
        )
    def test_movie_search(self, mock_fetch_movie, mock_movie_parse_response):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        # Check invaild input.
        with self.assertRaises(AssertionError):
            movie.movie_search(None, {})

        self.assertEqual(movie.movie_search("abc", {}), ["a", "b"])

    def mocked_requests_get_200(*args, **kwargs):
        return MockResponse({"key1": "value1"}, 200)
    
    def mocked_requests_get_else(*args, **kwargs):
        return MockResponse(None, 401)

    @unittest.mock.patch("requests.get", side_effect=mocked_requests_get_200)
    def test_fetch_movie(self, mock_get):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        movie_name1 = "harry potter"
        movie.fetch_movie(movie_name=movie_name)
        self.assertEqual(
            movie.search_query,
            "https://api.themoviedb.org/3/search/movie?query=harry%20potter&"\
                "language=en-US&page=1"
            )

        response = movie.fetch_movie(movie_name1)
        self.assertIsInstance(response, dict)

    @unittest.mock.patch("requests.get", side_effect=mocked_requests_get_else)
    def test_fetch_movie(self, mock_get):
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True):
            movie = Movie()

        movie_name = "abc"
        movie.fetch_movie(movie_name=movie_name)
        response = movie.fetch_movie(movie_name)
        self.assertIsInstance(response, dict)
        

    # def test_fetch_collection(self):
    #     pass

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