import os
import requests
import json
from PIL import Image
import os 

class Movie:
    def __init__(self):
        self.name = None
        self.__TMDB_API_KEY = os.getenv("TMDB_API_KEY")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        with open(os.path.join(dir_path, "config.json"), "r") as file:
            self.config = json.load(file)

        self.url = self.config["basic_url"]
        self.header = self.config["header"]
        self.header["Authorization"] += self.__TMDB_API_KEY

        self.test_api_connection(self.url, self.__TMDB_API_KEY)

    def movie_search(
            self, movie_name:str=None, user_preference={}, *args, **kwargs
            ):
        mv_basic_response = self.fetch_movie(movie_name)
        movies = self.movie_parse_response(
            movie_response=mv_basic_response,
            num_results=user_preference["num_results"],
            genre=user_preference["movie_genre"]
            )

        return movies

    def fetch_movie(self, movie_name:str=None):
        # Fetch basic movie information.
        try:
            # Make a GET request
            endpoint = self.config["search_endpoint"]
            movie_name = movie_name.replace(" ", "%20")

            query = f"{self.url}{endpoint}?query={movie_name}&language=en-US&page=1"
            print(query)
            mv_basic_response = requests.get(query, headers=self.header)

            if mv_basic_response.status_code == 200:
                print("Data fetched successfully!")
                mv_basic_response = mv_basic_response.json()
                return mv_basic_response
            else:
                print(f"Failed to fetch data. HTTP status code: {mv_basic_response.status_code}")
                print("Response:", mv_basic_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def fetch_collection(self, id):
        """Fetch movie homepage."""

        try:
            # Make a GET request
            endpoint = self.config["collection_endpoint"].replace("MOVIE_ID", str(id))

            query = f"{self.url}{endpoint}"
            print(query)
            mv_col_response = requests.get(query, headers=self.header)

            if mv_col_response.status_code == 200:
                print("Data fetched successfully!")
                mv_col_response = mv_col_response.json()
                return mv_col_response
                
            else:
                print(f"Failed to fetch data. HTTP status code: {mv_col_response.status_code}")
                print("Response:", mv_col_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def movie_parse_response(
            self, movie_response:dict, num_results:int=3, 
            genre_preference:list=None, is_recom:bool=False, 
            *args, **kwargs
        ):
        movies = []
        count = 0
        if movie_response:
            results = movie_response["results"]
            for res in results:
                if (count >= num_results) or (genre_preference is not None and genre_preference not in res["genre_ids"]):
                    continue
                else:
                    movie_info = {}
                    movie_info["id"] = res.get("id", None)
                    movie_info["original_language"] = res.get("original_language", None)
                    movie_info["original_title"] = res.get("original_title", None)
                    movie_info["overview"] = res.get("overview", None)
                    movie_info["release_date"] = res.get("release_date", None)
                    movie_info["backdrop_path"] = res.get("backdrop_path", None)
                    movie_info["poster_path"] = res.get("poster_path", None)
                    movie_info["genre_ids"] = res.get("genre_ids", [])
                    movie_info["collection"] = None

                    if movie_info["poster_path"]:
                        movie_info["poster_url"] = \
                            f"https://image.tmdb.org/t/p/w154{\
                                movie_info["poster_path"]}"

                    if movie_info["backdrop_path"]:
                        movie_info["backdrop_url"] = \
                            f"https://image.tmdb.org/t/p/w500{\
                                movie_info["backdrop_path"]}"
                        
                    if movie_info["genre_ids"]:
                        names = []
                        for id in movie_info["genre_ids"]:
                            names += [self.config["MOVIE_GENRES_NUMBER_NAME"][str(id)]]
                        movie_info["genre_names"] = names

                    # Get collections.
                    # if not is_recom:
                    collection_response = self.fetch_collection(movie_info["id"])
                    if collection_response["belongs_to_collection"]:
                        movie_info["collection"] = collection_response["belongs_to_collection"]["name"]
                        movie_info["collection_poster_path"] = collection_response["belongs_to_collection"]["poster_path"]
                        if movie_info["collection_poster_path"]:
                            movie_info["collection_poster_url"] = \
                                f"https://image.tmdb.org/t/p/w154{\
                                    movie_info["collection_poster_path"]}"
                        
                    movie_info["homepage"] = collection_response["homepage"]

                    movies.append(movie_info) 
                    count += 1  
        else:
            print("Sorry, Couldn't find the movie.")
        return movies[:num_results]

    def movie_recom(self, recom_preference: dict[str, any]):
        recoms_response = self.fetch_recom()
        movie_recoms = self.movie_parse_response(
            movie_response=recoms_response,
            num_results=recom_preference["num_recom"],
            genre_preference=recom_preference["genre"],
            is_recom=True
            )
        
        return movie_recoms

    def fetch_recom(self):
        """Fetch movie recommadation based on search movie."""
        try:
            # Make a GET request
            endpoint = self.config["recommendation_endpoint"]

            query = f"{self.url}{endpoint}"
            print(query)
            mv_recom_response = requests.get(query, headers=self.header)

            if mv_recom_response.status_code == 200:
                print("Data fetched successfully!")
                mv_recom_response = mv_recom_response.json()
                return mv_recom_response
                
            else:
                print(f"Failed to fetch data. HTTP status code: {mv_recom_response.status_code}")
                print("Response:", mv_recom_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        return None

    def test_api_connection(self, api_url, api_key):
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
                print("Connection successful and API key is valid.")
                return True
            elif response.status_code == 401:
                print("Invalid API key. Please check your API credentials.")
            else:
                print(f"Connection failed. HTTP status code: {response.status_code}")
                print("Response:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
        return False


if __name__ == "__main__":
    movie = Movie()
    # response = movie.movie_search("Harry Potter", {"num_results": 3})
    # mv_list = movie.movie_parse_response(response)

    recom_pref = {"num_recom": 3, "genre": None}
    recom_response = movie.movie_recom(recom_pref)

    print(recom_response)

