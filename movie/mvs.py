from PIL import Image
from io import BytesIO
import requests
from IPython.display import display
from termcolor import colored

from movie.movie import Movie
from music_user.music import Music
from music_user.user import User

class MVS(Movie, Music):
    def __init__(self):
        super().__init__()
        self.movie = Movie()
        self.music = Music()
        self.preference = None

    def return_movie_results(
            self, movie_name: str, user_preference: str=None, *args, **kwargs
            ):
        
        # Search movie information.
        mo_results = self.movie.movie_search(
            movie_name, user_preference, *args, **kwargs
            )
        
        return mo_results

    def return_music_results(
            self, movie_name: str, user_preference: str=None, *args, **kwargs
            ):
        # Search music information.
        mu_results = self.music.music_search(
            movie_name, user_preference, *args, **kwargs
            )
        
        return mu_results

    def return_recom(self, recom_preference: dict[str, any]):
        mo_recom_results = None
        mu_recom_results = None

        if recom_preference["recom_type"] == "movie":
            mo_recom_results = self.movie.movie_recom(recom_preference)
            return mo_recom_results, []
        elif recom_preference["recom_type"] == "music":
            mu_recom_results = self.music.music_recom(recom_preference)
            return [], mu_recom_results
        else:
            mo_recom_results = self.movie.movie_recom(recom_preference)
            mu_recom_results = self.music.music_recom(recom_preference)
            return mo_recom_results, mu_recom_results

    def display_movie_details(self, movie_info):
        # Display poster.
        Image.open(requests.get(movie_info["poster_url"], stream=True).raw)
        print(colored(movie_info["original_title"], "green"))
        if movie_info["poster_url"]:
            img_reponse = requests.get(movie_info["poster_url"])
            img = Image.open(BytesIO(img_reponse.content))
            display(img)

        if movie_info["overview"]:
            print(colored(movie_info["overview"], 'yellow'))

        if movie_info["homepage"]:
            print(f"Homepage: {movie_info["homepage"]}")
        else:
            print(f"Homepage: Sorry there is no available link. -.-")

        if movie_info["release_date"]:
            print(f"Release Date: {movie_info["release_date"]}")
        else:
            print(f"Release Date: Unknown.")

        if movie_info["genre_names"]:
            print(f"Genre: {movie_info["genre_names"]}")
        
        if movie_info["collection"]:
            print(f"Belongs to collection: {movie_info["collection"]}")
            if movie_info["collection_poster_url"]:
                img_reponse = requests.get(movie_info["collection_poster_url"])
                img = Image.open(BytesIO(img_reponse.content))
                display(img)

        # For pretty print.
        print()
    
    def display_music_details(self, music_info):
        print("--------- MUSIC ---------")
        print()
        pass

    def start(self):
        # Get user inputs
        user = User()
        user.user_input()

        # Get preference
        self.preference = user.preference
        movie_name = user.movie_name

        movie_results = self.return_movie_results(movie_name, self.preference)
        # music_results = self.return_music_results(movie_name, self.preference)

        # If user wants recommendation, return it.
        if self.preference["is_recom"]:
            mv_recom_results, mu_recom_results = self.return_recom(self.preference["is_recom"])

        """Display results"""
        # Display movie results.
        for item in movie_results:
            self.display_movie_details(item)
        
        print("---------- Movie Recommendation For Today ------------")
        if self.preference["is_recom"]:
            for item in mv_recom_results:
                self.display_movie_details(item)

