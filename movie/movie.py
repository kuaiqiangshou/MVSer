import os
import requests
import json
import os 

class Movie:
    """Movie module to call TMDB API.
    """

    def __init__(self):
        """Initial function of Movie class.
        """

        self.name = None
        # Get user TMDB API Key from environment variable.
        self.__TMDB_API_KEY = os.getenv("TMDB_API_KEY")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        # Load configuration file.
        with open(os.path.join(dir_path, "config.json"), "r") as file:
            self.config = json.load(file)

        self.url = self.config["basic_url"]
        self.header = self.config["header"]
        self.header["Authorization"] += self.__TMDB_API_KEY

        # Test api connection.
        self.test_api_connection(self.url, self.__TMDB_API_KEY)

    def movie_search(
            self, movie_name:str=None, user_preference:dict={}) -> list:
        """Search movie inforamtion from TMDB by calling API using user input.

        Args:
            movie_name (str, optional): The movie name. Defaults to None.
            user_preference (dict, optional): A dictionary of user perference. 
                Defaults to {}.

        Returns:
            list: A list of movies information related to user input.
        """
        mv_basic_response = self.fetch_movie(movie_name)
        movies = self.movie_parse_response(
            movie_response=mv_basic_response,
            num_results=user_preference["num_results"],
            genre_preference=user_preference["movie_genre"]
            )

        return movies

    def fetch_movie(self, movie_name:str=None) -> dict[str:any]:
        """Fetch basic movie information.

        Returns:
            list: The list of responses.
        """

        try:
            # Make a GET request
            endpoint = self.config["search_endpoint"]

            # Remove blank space and replace them to %20.
            movie_name = movie_name.replace(" ", "%20")

            query = f"{self.url}{endpoint}?query={movie_name}\
                &language=en-US&page=1"
            mv_basic_response = requests.get(query, headers=self.header)

            if mv_basic_response.status_code == 200:
                # print("Data fetched successfully!")
                mv_basic_response = mv_basic_response.json()
                return mv_basic_response
            else:
                print(
                    f"Failed to fetch data. HTTP status code: \
                        {mv_basic_response.status_code}"
                    )
                print("Response:", mv_basic_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def fetch_collection(self, id: str="") -> dict[str: any]:
        """Fetch related movie collection and homepage from movie id.

        Args:
            id (str, optional): The movie id. Defaults to "".

        Returns:
            dict: response dictionary.
        """

        try:
            # Make a GET request
            endpoint = self.config["collection_endpoint"] \
                .replace("MOVIE_ID", str(id))

            query = f"{self.url}{endpoint}"
            mv_col_response = requests.get(query, headers=self.header)

            if mv_col_response.status_code == 200:
                # print("Data fetched successfully!")
                mv_col_response = mv_col_response.json()
                return mv_col_response
                
            else:
                print(
                    f"Failed to fetch data. HTTP status code: \
                        {mv_col_response.status_code}"
                    )
                print("Response:", mv_col_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def movie_parse_response(
            self, movie_response:dict, num_results:int=3, 
            genre_preference:list=None, is_recom:bool=False, 
        ) -> list:
        """Parse API response.

        Args:
            movie_response (dict): The response from API call.
            num_results (int, optional): The number of results to return. 
                Defaults to 3.
            genre_preference (list, optional): The user preference for genre. 
                Defaults to None.
            is_recom (bool, optional): A indicator whether parsing the 
                recommandation response or not. We only provide collection 
                information for non-recommand movies. Defaults to False.

        Returns:
            list: A list of return results that are organized in a dictionary 
                    format.
        """
        movies = []
        count = 0
        if movie_response:
            results = movie_response["results"]
            for res in results:
                if (count >= num_results) or \
                    (
                        genre_preference is not None and \
                            genre_preference not in res["genre_ids"]
                    ):
                    continue
                else:
                    movie_info = {}
                    movie_info["id"] = res.get("id", None)
                    movie_info["original_language"] = res.get(
                        "original_language", None
                        )
                    movie_info["original_title"] = res.get(
                        "original_title", None
                        )
                    movie_info["overview"] = res.get("overview", None)
                    movie_info["release_date"] = res.get(
                        "release_date", None
                        )
                    movie_info["backdrop_path"] = res.get(
                        "backdrop_path", None
                        )
                    movie_info["poster_path"] = res.get("poster_path", None)
                    movie_info["genre_ids"] = res.get("genre_ids", [])
                    movie_info["collection"] = None

                    if movie_info["poster_path"]:
                        movie_info["poster_url"] = \
                            f"https://image.tmdb.org/t/p/w500{\
                                movie_info["poster_path"]}"

                    if movie_info["backdrop_path"]:
                        movie_info["backdrop_url"] = \
                            f"https://image.tmdb.org/t/p/w500{\
                                movie_info["backdrop_path"]}"
                        
                    if movie_info["genre_ids"]:
                        names = []
                        for id in movie_info["genre_ids"]:
                            names += [
                                self.config[
                                    "MOVIE_GENRES_NUMBER_NAME"
                                    ][str(id)]
                                    ]
                        movie_info["genre_names"] = names

                    # Get collections.
                    collection_response = self.fetch_collection(
                        movie_info["id"]
                        )
                    if not is_recom:
                        if collection_response["belongs_to_collection"]:
                            movie_info["collection"] = collection_response[
                                "belongs_to_collection"
                                ]["name"]
                            movie_info["collection_poster_path"] = \
                                collection_response["belongs_to_collection"][
                                    "poster_path"
                                    ]
                            if movie_info["collection_poster_path"]:
                                movie_info["collection_poster_url"] = \
                                    f"https://image.tmdb.org/t/p/w500{\
                                        movie_info["collection_poster_path"]}"
                        
                    movie_info["homepage"] = collection_response["homepage"]

                    movies.append(movie_info) 
                    count += 1  
        else:
            print("Sorry, Couldn't find the movie.")
        return movies[:num_results]

    def movie_recom(self, recom_preference: dict[str, any]) -> list:
        """Get movie recommandation.

        Args:
            recom_preference (dict[str, any]): The preference dictionary.       

        Returns:
            list: A list of recommandation movies.
        """
        recoms_response = self.fetch_recom()
        movie_recoms = self.movie_parse_response(
            movie_response=recoms_response,
            num_results=recom_preference["num_recom"],
            genre_preference=recom_preference["genre"],
            is_recom=True
            )
        
        return movie_recoms

    def fetch_recom(self) -> dict[str, any]:
        """Fetch movie recommadation based on search movie."""
        try:
            # Make a GET request
            endpoint = self.config["recommendation_endpoint"]

            query = f"{self.url}{endpoint}"
            mv_recom_response = requests.get(query, headers=self.header)

            if mv_recom_response.status_code == 200:
                # print("Data fetched successfully!")
                mv_recom_response = mv_recom_response.json()
                return mv_recom_response
                
            else:
                print(
                    f"Failed to fetch data. HTTP status code: \
                        {mv_recom_response.status_code}"
                    )
                print("Response:", mv_recom_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def test_api_connection(self, api_url, api_key) -> bool:
        """
        Test API connection and validate API key.
        
        Parameters:
            api_url (str): Base URL of the API.
            api_key (str): API key for authentication.
        
        Returns:
            bool: True if the connection is successful and API key is valid, False otherwise.
        """
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            # Send a test GET request to check connection
            response = requests.get(f"{api_url}/authentication", headers=headers)

            if response.status_code == 200:
                # print("Connection successful and API key is valid.")
                return True
            elif response.status_code == 401:
                print("Invalid API key. Please check your API credentials.")
            else:
                print(f"Connection failed. HTTP status code: {response.status_code}")
                print("Response:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
        return False
