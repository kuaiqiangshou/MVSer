class User:
    def __init__(self):
        self.preference = None
        self.movie_name = None

    def user_input(self):
        self.movie_name = "Frozen"
        self.preference = {
            "num_results": 1,
            "music_version": "clean",
            "movie_genre": None,
            "music_genre": None,
            "is_recom": {
                "recom_type": "Both", 
                "num_recom": 1,
                "genre": None
                }
        }
    
    def check_inputs(self, user_preference: dict):
        pass

    def display_preference(self):
        pass
