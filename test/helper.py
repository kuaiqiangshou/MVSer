import requests

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def mocked_requests_get_200(*args, **kwargs):
    return MockResponse({"key1": "value1"}, 200)

def mocked_requests_get_else(*args, **kwargs):
    return MockResponse(None, "401")

def mocked_resquests_get_request_exception(*args, **kwargs):
    raise requests.exceptions.RequestException

def mocked_resquests_get_exception(*args, **kwargs):
    raise Exception
