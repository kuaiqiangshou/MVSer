from PIL import Image
from io import BytesIO
import requests
from IPython.display import display
from datetime import datetime

PRINT_MOOD = ""
try:
    import emoji
except ModuleNotFoundError:
    print(
        "Warning: module 'emoji' is not installed. For best visual experience"
        ", please install emoji by run 'pip install emoji'. More detail, please"
        " see https://pypi.org/project/emoji/"
            )
    PRINT_MOOD = "simple"

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
            ) -> dict:
        """Search movie information

        Args:
            movie_name (str, optional): The input movie name. Defaults to "".
            user_preference (str, optional): The user preference for search. 
            Defaults to None.

        Returns:
            dict: A dictionary of movies details, which keys are movie names 
                and values are the movie details.
        """
        
        # Search movie information.
        mo_infos = self.movie.movie_search(
            movie_name, user_preference, *args, **kwargs
            )
        
        mo_results = {}
        for item in mo_infos:
            mo_results[item["original_title"]] = item
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
        self.decoration(
            emo=":bright_button:", info=movie_info["original_title"], 
            mode="title"
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
        # Display title.
        self.decoration(
            emo=":bright_button:", info=music_info["name"], mode="title"
            )

        # Display poster.
        if music_info["img_url"]:
            img_reponse = requests.get(music_info["img_url"])
            img = Image.open(BytesIO(img_reponse.content))
            display(img)

        if music_info["album_urls"]:
            print(f"Album: {music_info["album_urls"]}")
        else:
            print(f"Album: Sorry there is no available link. -.-")

        if music_info["artists"]:
            print(f"Artists: {music_info["artists"]}")

        if music_info["release_date"]:
            print(f"Release Date: {music_info["release_date"]}")
        else:
            print(f"Release Date: Unknown.")

        # For pretty print.
        print()

    def start(self) -> None:
        """Start function for MVSer package.
        """
        # Get user inputs
        user = User()
        user.user_input()

        # Display user preference.
        self.decoration(
                    emo=":star:",
                    info=f"User Preference"
                    )
        user.display_preference()
        print()

        # Get preference
        self.preference = user.preference
        user_mv_name_query = user.movie_name

        # Get movie results.
        movie_results = self.return_movie_results(
            user_mv_name_query, self.preference
            )
        if not movie_results:
            self.decoration(
                emo=":loudly_crying_face:", 
                info=f"Sorry, there is no matched movie!"
                )

        # Get related music results.
        music_results_dic = {}
        for name, _ in movie_results.items():
            music_results = self.return_music_results(name, self.preference)
            music_results_dic[name] = music_results

        # Recommendations.
        if self.preference["is_recom"]:
            mv_recom_results, mu_recom_results = self.return_recom(
                self.preference["is_recom"]
                )

        """Display results"""
        # Display movie results.
        for name, movie_details in movie_results.items():
            self.decoration(
                emo=":movie_camera:",
                info=f"Movie Details for {name}"
                )
            	
            self.display_movie_details(movie_details)
            
            self.decoration(
                emo=":musical_notes:",
                info=f"Music Album in {name}"
                )
            for music_res in music_results_dic[name]:
                self.display_music_details(music_res)
        
        if self.preference["is_recom"]:
            if mv_recom_results:
                self.decoration(
                    emo=":star:",
                    info=f"Movies You May Like For {datetime.today().strftime('%Y-%m-%d')}"
                    )
                for item in mv_recom_results:
                    self.display_movie_details(item)
            
            if mu_recom_results:
                self.decoration(
                    emo=":star:",
                    info=f"Music You May Like"
                    )
                for item in mu_recom_results:
                    self.display_music_details(item)

    def decoration(self, emo: str="", info: str="", mode: str="") -> None:
        """Pretty print function

        Args:
            info (str, optional): The printing string. Defaults to "".
        """

        len_content = len(info)

        if mode == "title":
            nb_emo = 1
        else:
            nb_emo = min(len_content, 18)

        if PRINT_MOOD == "simple":
            line = f"{'**' * nb_emo}"
        else:
            line = f"{emoji.emojize(emo * nb_emo)}"

        print(f"{line} {info} {line}")
        print()
