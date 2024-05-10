''''''

import os
import json
import time
import logging
import threading
import subprocess


class TokenManager:
    def __init__(self):

        self.COPERNICUS_USERNAME = os.getenv("COPERNICUS_USERNAME", None)
        self.COPERNICUS_PASSWORD = os.getenv("COPERNICUS_PASSWORD", None)

        if not self.COPERNICUS_USERNAME or not self.COPERNICUS_PASSWORD:
            raise ValueError("COPERNICUS_USERNAME and COPERNICUS_PASSWORD must be set in the environment variables")

        self.token_start_time = None
        self.token_duration = None

        self.token_refresh_time_buffer = 10

        self.logger = logging.getLogger()



    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def get_headers(self) -> dict:
        return 

        
    def start(self):
        """ Starts the token manager
        
        :params: None
        :return: None
        """

        self.generate_acess_token()
        self.logger.info("Token manager started")



    def generate_acess_token(self) -> None:
        """ Generates the access token for the Copernicus API, firstly it
        generates the main token and then starts a scheduler to refresh the
        token periodically
        
        :params: None
        :return: None
        """

        # Cli command to generate the main token
        token_command = f"curl --location --request POST 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token' \
                            --header 'Content-Type: application/x-www-form-urlencoded' \
                            --data-urlencode 'grant_type=password' \
                            --data-urlencode 'username={self.COPERNICUS_USERNAME}' \
                            --data-urlencode 'password={self.COPERNICUS_PASSWORD}' \
                            --data-urlencode 'client_id=cdse-public'\
                        "
        
        # Generate the main token
        self.logger.info("Generating main token")
        response = subprocess.check_output(token_command, shell=True)
        response = json.loads(response)
        self.logger.info("Main token generated")

        # Extract the refresh token and the main token
        self.refresh_token = response["refresh_token"]
        self.token = response["access_token"]

        # Extract the token duration and the refresh token duration
        self.token_start_time = time.time()
        self.token_duration = response["expires_in"]
        self.refresh_token_duration = response["refresh_expires_in"]

        # Calculate the time to refresh the token
        refresh_time = self.refresh_token_duration - self.token_refresh_time_buffer

        # Start the token scheduler
        self.logger.info(f"Token will be refreshed in {refresh_time} seconds")
        self.start_token_scheduler(refresh_time)
        self.logger.info("Token scheduler started")



    def regenerate_token(self):
        """ Regenerates the token using the refresh token
        
        :params: None
        :return: None
        """

        # Cli command to refresh the token
        token_command = f"curl --location --request POST 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token' \
                            --header 'Content-Type: application/x-www-form-urlencoded' \
                            --data-urlencode 'grant_type=refresh_token' \
                            --data-urlencode 'refresh_token={self.refresh_token}' \
                            --data-urlencode 'client_id=cdse-public'"

        # Refreshing the token
        self.logger.info("Refreshing token")
        response = subprocess.check_output(token_command, shell=True)
        response = json.loads(response)

        try:
            self.token = response["access_token"]
            self.refresh_token = response["refresh_token"]
        except KeyError as e:
            self.logger.error("Error refreshing token: {e}")
            return
        
        self.logger.info("Token refreshed correctly")



    def start_token_scheduler(self, refresh_time: int = 3600):
        """ Starts a scheduler to refresh the token periodically
        
        :params: refresh_time: int - Time in seconds to refresh the token
        :return: None
        """

        def token_scheduler():
            while True:
                time.sleep(refresh_time)
                self.regenerate_token()

        # Start the token scheduler in the background
        scheduler_thread = threading.Thread(target=token_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

