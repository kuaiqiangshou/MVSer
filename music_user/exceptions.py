# exceptions.py

class APICallError(Exception):
    def __init__(self, status_code, message: str = "", *args):
        super().__init__(*args)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return repr(
            f"Failed to fetch data. HTTP status code: {self.status_code}. "
            f"{self.message}" if self.status_code else f"Unknown error occurred."
        )

class InvalidGenreError(Exception):
    def __init__(self, genre: str = "", *args):
        super().__init__(*args)
        self.genre = genre

    def __str__(self):
        return repr(
            f"Invalid genre specified: '{self.genre}'. Please provide a valid genre."
        )