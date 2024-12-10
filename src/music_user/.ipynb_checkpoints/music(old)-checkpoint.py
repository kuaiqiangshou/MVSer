# music(old).py

import os
import requests
import json
from dotenv import load_dotenv

class Music:
    """Music module to call Spotify API."""

    def __init__(self):
        """Initial function of Music class."""
        self.name = None

        # Load Spotify API Key from environment variables
        dir_path = os.path.dirname(os.path.realpath(__file__))
        load_dotenv(os.path.join(dir_path, ".env"))
        self.__SPOTIFY_API_KEY = os.getenv("SPOTIFY_API_KEY")

        if not self.__SPOTIFY_API_KEY:
            raise ValueError("SPOTIFY_API_KEY is missing. Please set it in your .env file.")

        # Load configuration file
        with open(os.path.join(dir_path, "config.json"), "r") as file:
            self.config = json.load(file)

        self.url = self.config["basic_url"]
        self.header = self.config["header"]
        self.header["Authorization"] += self.__SPOTIFY_API_KEY

        # Test API connection
        self.test_api_connection()

    def test_api_connection(self) -> bool:
        """Test API connection and validate API key."""
        try:
            response = requests.get(f"{self.url}/browse/categories", headers=self.header)
            if response.status_code == 200:
                print("Spotify API connection successful.")
                return True
            elif response.status_code == 401:
                raise ValueError("Invalid Spotify API key.")
            else:
                print(f"API connection failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Spotify API: {e}")
        return False

    def music_search(self, movie_name: str = None, user_preference: dict = {}) -> list:
        """
        Search music information from Spotify API using user input.

        Args:
            movie_name (str, optional): The movie name. Defaults to None.
            user_preference (dict, optional): A dictionary of user preferences. Defaults to {}.

        Returns:
            list: A list of music information related to user input.
        """
        try:
            music_response = self.fetch_music(movie_name)
            return self.music_parse_response(
                music_response=music_response,
                num_results=user_preference.get("num_results", 3)
            )
        except Exception as e:
            print(f"Error during music search: {e}")
            return []

    def fetch_music(self, movie_name: str = None) -> dict:
        """
        Fetch basic music information from Spotify API.

        Args:
            movie_name (str): The movie name.

        Returns:
            dict: The response dictionary from the Spotify API.
        """
        try:
            endpoint = self.config["track_search_endpoint"]
            query = f"{self.url}{endpoint}?q={movie_name.replace(' ', '%20')}+soundtrack&type=track&limit=10"
            response = requests.get(query, headers=self.header)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching music data: {e}")
            return {}

    def music_recom(self, recom_preference: dict = {}) -> list:
        """
        Get music recommendations.

        Args:
            recom_preference (dict): The user preferences dictionary.

        Returns:
            list: A list of recommended music tracks.
        """
        try:
            recom_response = self.fetch_recommendations(recom_preference)
            return self.music_parse_response(
                music_response=recom_response,
                num_results=recom_preference.get("num_recom", 3)
            )
        except Exception as e:
            print(f"Error during music recommendations: {e}")
            return []

    def fetch_recommendations(self, recom_preference: dict) -> dict:
        """
        Fetch music recommendations based on user input.

        Args:
            recom_preference (dict): The user preference dictionary.

        Returns:
            dict: The response dictionary from the Spotify API.
        """
        try:
            genre = recom_preference.get("genre", "pop")
            endpoint = self.config["genre_recommendations_endpoint"]
            params = {
                "seed_genres": genre,
                "limit": recom_preference.get("num_recom", 3)
            }
            query = f"{self.url}{endpoint}"
            response = requests.get(query, headers=self.header, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recommendations: {e}")
            return {}

    def music_parse_response(self, music_response: dict, num_results: int = 3) -> list:
        """
        Parse API response to extract music details.

        Args:
            music_response (dict): The API response.
            num_results (int, optional): The number of results to return. Defaults to 3.

        Returns:
            list: A list of dictionaries with music details.
        """
        tracks = music_response.get("tracks", {}).get("items", [])
        music_results = []
        for track in tracks[:num_results]:
            track_info = {
                "track_name": track.get("name"),
                "artist": track["artists"][0]["name"],
                "album": track.get("album", {}).get("name"),
                "release_date": track.get("album", {}).get("release_date"),
                "preview_url": track.get("preview_url", "No preview available.")
            }
            music_results.append(track_info)
        return music_results