import unittest
from test.movie import TestMovie
from test.movie import TestMVS

def test_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(TestMovie("test_init_success"))
    suite.addTest(TestMovie("test_init_fail"))
    suite.addTest(TestMovie("test_movie_search"))
    suite.addTest(TestMovie("test_fetch_movie_success"))
    suite.addTest(TestMovie("test_fetch_movie_fails"))
    suite.addTest(TestMovie("test_fetch_collection_success"))
    suite.addTest(TestMovie("test_fetch_collection_fails"))
    suite.addTest(TestMovie("test_movie_parse_response"))
    suite.addTest(TestMovie("test_movie_recom"))
    suite.addTest(TestMovie("test_fetch_recom_success"))
    suite.addTest(TestMovie("test_fetch_recom_fail"))
    suite.addTest(TestMovie("test_test_api_connection_success"))
    suite.addTest(TestMovie("test_test_api_connection_fail"))
    suite.addTest(TestMVS("test_init_success"))
    suite.addTest(TestMVS("test_return_movie_results"))
    suite.addTest(TestMVS("test_return_music_results"))
    suite.addTest(TestMVS("test_return_recom"))
    suite.addTest(TestMVS("test_display_movie_details"))
    suite.addTest(TestMVS("test_display_music_details"))
    suite.addTest(TestMVS("test_decoration"))
    return suite


if __name__ == "__main__":
    suite = test_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)