import warnings

class APICallError(Exception):
    def __init__(self, status_code, *args):
        super().__init__(*args)
        self.status_code = status_code

    def __str__(self):
        return(repr(
            f"Failed to fetch data. HTTP status code:"\
            "{self.status_code}."
            )
        )

class MovieIDEmptyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

      