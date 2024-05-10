


import time
import logging
import requests

from src.token_manager import TokenManager

class APIManager:
    """
    Class to manage the API requests to the Copernicus API, it automanages the
    token generation and expiration

    This class manages all communication with the Copernicus API, handeling the
    token authentication and refreshing in the background. 
    
    This class is a singleton, so it should be instantiated only once.
    """



    def __init__(self):

        self.logger = logging.getLogger()

        self.token_manager = TokenManager()
        self.token_manager.start()


    def make_request(self, url:str, params:dict={}, headers:dict=None) -> requests.models.Response:
        """
        Sends an specified request to the Copernicus API returning the response
        (as a requests.models.Response object)

        Parameters
        ----------
        url : str
            URL of the request

        params : dict, optional
            Parameters to send in the request, by default {}

        headers : dict, optional
            Headers to send in the request, by default None, if None, it uses
            the token headers
        
        Returns
        -------
        requests.models.Response
            Response of the request
        """

        headers = self.headers if not headers else headers

        response = requests.get(url, headers=self.headers, params=params)
        return response
    

    def get_image(self, image_url:str, params:dict=None) -> tuple[requests.models.Response, int]:
        """
        Gets an image from the Copernicus API and returns the response as a
        stream and the total size of the response.

        No headers are needed for this request, as the token is strictly
        necessary for the authentication.

        Parameters
        ----------
        image_url : str
            URL of the image to download

        params : dict, optional
            Parameters to send in the request, by default None
        
        Returns
        -------
        tuple : requests.models.Response, int
            Tuple with the response stream and the total size of the response

        """


        response = requests.get(image_url, stream=True, headers=self.headers, params=params)

        # If the response is not 200, log the error and return None
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None, 0

        response_size = int(response.headers.get('content-length', 0))

        return response, response_size


    @property
    def headers(self):
        return self.token_manager.headers