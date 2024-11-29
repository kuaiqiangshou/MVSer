from PIL import Image
from io import BytesIO
import requests
from IPython.display import display
from termcolor import colored
from datetime import datetime
import emoji

from movie.movie import Movie
from music_user.music import Music
from music_user.user import User

class MVS(Movie, Music):
    """Used to connect Movie and Music classes."""
    def __init__(self):
        """Initial function of MVS class."""

        super().__init__()
        self.movie = Movie()
        self.music = Music()
        self.preference = None

    def return_movie_results(
            self, movie_name: str="", user_preference: str=None, *args, **kwargs
            ) -> list:
        """Search movie information

        Args:
            movie_name (str, optional): The input movie name. Defaults to "".
            user_preference (str, optional): The user preference for search. 
            Defaults to None.

        Returns:
            list: A list of movies details.
        """
        
        # Search movie information.
        mo_results = self.movie.movie_search(
            movie_name, user_preference, *args, **kwargs
            )
        
        return mo_results

    def return_music_results(
            self, movie_name: str="", user_preference: str=None, *args, **kwargs
            ) -> list:
        """Search relavant music results.

        Args:
            movie_name (str): The user input, movie name. Defaults to "".
            user_preference (str, optional): The user preference for results.
                Defaults to None.

        Returns:
            list: A list of music details.
        """
        # Search music information.
        mu_results = self.music.music_search(
            movie_name, user_preference, *args, **kwargs
            )
        
        return mu_results

    def return_recom(self, recom_preference: dict[str, any]=None) -> \
        tuple[list, list]:
        """Return a list of recommandation.

        Args:
            recom_preference (dict[str, any], optional): The recommadation 
                preference from user input. Defaults to None.

        Returns:
            tuple[list, list]: A list of movie recommadations, 
                a list of music recommadations.
        """

        mo_recom_results = None
        mu_recom_results = None

        if recom_preference["recom_type"] == "movie":
            # return movie recommandations.
            mo_recom_results = self.movie.movie_recom(recom_preference)
            return mo_recom_results, []
        elif recom_preference["recom_type"] == "music":
            # return music recommandations.
            mu_recom_results = self.music.music_recom(recom_preference)
            return [], mu_recom_results
        else:
            # return recommandations for both.
            mo_recom_results = self.movie.movie_recom(recom_preference)
            mu_recom_results = self.music.music_recom(recom_preference)
            return mo_recom_results, mu_recom_results

    def display_movie_details(self, movie_info: dict[str, any]={}) -> None:
        """Display movie details.

        Args:
            movie_info (dict[str, any]): The API response from movie search 
                results. Defaults to {}.
        """

        # Display title.
        print(emoji.emojize(":bright_button:"), " ", \
              colored(movie_info["original_title"], "green")
                )

        # Display poster.
        if movie_info["poster_url"]:
            img_reponse = requests.get(movie_info["poster_url"])
            img = Image.open(BytesIO(img_reponse.content))
            display(img)

        if movie_info["overview"]:
            print(f"Overview: {movie_info["overview"]}")

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
    
    def display_music_details(self, music_info: dict[str:any]={}) -> None:
        """Display music details

        Args:
            music_info (dict[str, any]): The API response from music search 
                results. Defaults to {}.
        """
        print("--------- MUSIC ---------")
        print()
        pass

    def start(self) -> None:
        """Start function for MVSer package.
        """
        # Get user inputs
        user = User()
        user.user_input()

        # Get preference
        self.preference = user.preference
        movie_name = user.movie_name

        movie_results = self.return_movie_results(movie_name, self.preference)
        music_results = self.return_music_results(movie_name, self.preference)

        # If user wants recommendation, return it.
        if self.preference["is_recom"]:
            mv_recom_results, mu_recom_results = self.return_recom(
                self.preference["is_recom"]
                )

        """Display results"""
        # Display movie results.
        for item in movie_results:
            self.display_movie_details(item)
        
        self.decoration(
            f"Movies You May Like For {datetime.today().strftime('%Y-%m-%d')}"
            )
        if self.preference["is_recom"]:
            for item in mv_recom_results:
                self.display_movie_details(item)

    def decoration(self, info: str="") -> None:
        """Pretty print function

        Args:
            info (str, optional): The printing string. Defaults to "".
        """

        emo = ":star:"
        len_content = len(info)

        nb_emo = len_content * 2
        line = f"{emoji.emojize(emo*nb_emo)}"
        len_side = (nb_emo - len_content - 4) // 2

        print(f"{line[:len_side]} {info} {line[:len_side]}")
