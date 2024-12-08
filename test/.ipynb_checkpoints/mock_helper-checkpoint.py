# mock_helper.py

class MockResponse(dict):
    def __init__(self, json_data, status_code):
        super().__init__(json_data)
        self.status_code = status_code

    def json(self):
        return self

def mocked_requests_get_200(*args, **kwargs):
    return MockResponse({
        "albums": {
            "items": [
                {
                    "name": "Test Album",
                    "artists": [{"name": "Artist1"}],
                    "release_date": "2021",
                    "external_urls": {"spotify": "url1"},
                    "images": [{"url": "image1"}]
                }
            ]
        }
    }, 200)

def mocked_requests_get_else(*args, **kwargs):
    return MockResponse({"albums": {"items": []}}, 401)