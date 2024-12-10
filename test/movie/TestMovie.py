import unittest
import os
from unittest import mock
import unittest.mock

from src.movie.movie import Movie
from test.helper import *
    
class TestMovie(unittest.TestCase):   

    def setUp(self):
        self.maxDiff = None
        with unittest.mock.patch.object(
            Movie, "test_api_connection", return_value=True
            ):
                self.movie = Movie()
        
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(
            unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
        )
        return super().setUpClass()
    
    """Test init function."""
    def test_init_success(self):
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
        self.assertEqual(
            self.movie.config["poster_url"],
            "https://image.tmdb.org/t/p/w500"
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
        results = self.movie.movie_search(None, {})
        self.assertEqual(results, ["a", "b"])
        
        results = self.movie.movie_search("abc", {})
        self.assertEqual(results, ["a", "b"])

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

    """Test movie_parse_response function."""
    def test_movie_parse_response(self):

        # Test default.
        result = self.movie.movie_parse_response()
        self.assertEqual(result, [])

        response = {
            "results": [
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
            ],
        }
        
        # Test movie search scenario.
        with unittest.mock.patch.object(Movie,
            "fetch_collection", return_value = {
                "belongs_to_collection": {
                    "name": "abc",
                    "poster_path": "/collect/abc",
                },
                "homepage": "homepage"
            }
            ):
            result = self.movie.movie_parse_response(
                movie_response=response,
                num_results=1,
                genre_preference="Action",
                is_recom=False
                )
            
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertDictEqual(
                result[0], 
                {
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
            )

        with unittest.mock.patch.object(Movie,
            "fetch_collection", return_value = {
                "belongs_to_collection": {
                    "name": "abc",
                    "poster_path": "/collect/abc",
                },
                "homepage": "homepage"
            }
            ):
            result = self.movie.movie_parse_response(
                movie_response=response,
                num_results=1,
                genre_preference="comedy",
                is_recom=False
                )
            
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 0)

        # Test recommendation scenario.
        with unittest.mock.patch.object(Movie,
            "fetch_collection", return_value = {
                "belongs_to_collection": {
                    "name": "abc",
                    "poster_path": "/collect/abc",
                },
                "homepage": "homepage"
            }
            ):
            result = self.movie.movie_parse_response(
                    movie_response=response,
                    num_results=1,
                    genre_preference="Action",
                    is_recom=True
                    )
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertDictEqual(
                result[0], 
                {
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
                    "homepage": "homepage",
                    "collection": "",
                    "collection_poster_path": "",
                    "collection_poster_url": ""
                }
            )
        
        # Test no response scenario.
        result = self.movie.movie_parse_response(
                    movie_response=None,
                    num_results=1,
                    genre_preference="",
                    is_recom=True
                    )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    """Test movie_recom function."""
    @unittest.mock.patch.object(Movie, "fetch_recom", return_value = {})
    @unittest.mock.patch.object(
        Movie, "movie_parse_response", return_value = ["a", "b", "c"]
        )
    def test_movie_recom(
        self, mock_fetch_recom, mock_movie_parse_response
        ):
        # Test default value.
        results = self.movie.movie_recom()
        self.assertEqual(results, ["a", "b", "c"])
        
        # Test incorrect preference input.
        results = self.movie.movie_recom(recom_preference="abc")
        self.assertEqual(results, ["a", "b", "c"])

    """Test fetch_recom function."""
    def test_fetch_recom_success(self):
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            response = self.movie.fetch_recom()
            self.assertEqual(
                self.movie.recom_query,
                "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
                )

            self.assertIsInstance(response, dict)

    def test_fetch_recom_fail(self):
        # Other status_code. 
        with unittest.mock.patch(
            "requests.get", side_effect=("401")
            ):
            response = self.movie.fetch_recom()
            self.assertEqual(response, None)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_request_exception
            ):
            response = self.movie.fetch_recom()
            self.assertEqual(response, None)
 
        # Other error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_exception
            ):
            response = self.movie.fetch_recom()
            self.assertEqual(response, None)  
        
    """Test test_api_connection function."""
    @unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
    def test_test_api_connection_success(self):
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_200
            ):
            url = "https://api.themoviedb.org/3"
            api_key = os.environ["TMDB_API_KEY"]
            response = self.movie.test_api_connection(
                api_url=url, api_key=api_key)
            self.assertTrue(response)

    @unittest.mock.patch.dict(os.environ, {"TMDB_API_KEY": "abc"})
    def test_test_api_connection_fail(self):
        # Other status_code. 
        url = "https://api.themoviedb.org/3"
        api_key = os.environ["TMDB_API_KEY"]
        with unittest.mock.patch(
            "requests.get", side_effect=mocked_requests_get_else
            ):
            response = self.movie.test_api_connection(url, api_key)
            self.assertEqual(response, False)
        
        # Request error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_request_exception
            ):
            response = self.movie.test_api_connection(url, api_key)
            self.assertEqual(response, False)
 
        # Other error.
        with unittest.mock.patch(
            "requests.get",
            side_effect=mocked_resquests_get_exception
            ):
            response = self.movie.test_api_connection(url, api_key)
            self.assertEqual(response, False)  

    def tearDown(self):
        self.movie = None
    
    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()
        

if __name__ == "__main__":
    # run with python -m unittest ./test/movie/TestMovie.py
    unittest.main()