

from tqdm import tqdm

from config.request_templates import templates
from src.api_manager import APIManager



class ImageRequest():
    """
    A class to manage and format the image request to the Copernicus API.

    It makes several requests to the API to get the final image URL of the
    specified image_id. Several requests are needed because the API has an
    internal node structure in which the different image resolutions and bands
    are stored.

    The final URL is stored in the request attribute.

    Attributes
    ----------
    request : str
        URL of the final image request

    
    Methods
    -------
    get_final_image_url()
        Gets the final image URL of the specified image_id, storing it in the
        request attribute
    download_image(block_size=1024)
        Downloads the image from the API and returns a generator with the image
        data, yielding it in blocks of block_size bytes.
    
    """



    def __init__(self, image_id: str = None, api_manager: APIManager = None):
        """
        Parameters
        ----------
        image_id : str, optional
            ID of the image to get, by default None
        api_manager : APIManager, optional
            APIManager object to make the requests, by default None
        """

        self.request = templates.image_base_url.format(product_id=image_id)
        
        self.__api_manager = api_manager if api_manager else APIManager()
        self.__is_image_10m = False

        self.get_final_image_url()



    def get_final_image_url(self):
        """
        Finds the final image URL of the specified image_id, storing it in the
        \"request\" attribute

        By means of several requests to the Copernicus API, it gets the final
        URL, determining in the process if several resolutions of it are
        available or not.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """


        # Get image name
        response = self.__api_manager.make_request(self.request, 
                                                 params={})
        response = response.json()


        product_name = response['result'][0]['Name']

        self.request += f"({product_name})/Nodes(GRANULE)/Nodes"


        # Get GRANULE name
        response = self.__api_manager.make_request(self.request,
                                                params={})
        response = response.json()
        granule_name = response['result'][0]['Name']
        self.request += f"({granule_name})/Nodes(IMG_DATA)/Nodes"


        # Get image resolution
        response = self.__api_manager.make_request(self.request,
                                                params={})
        response = response.json()
        

        # Check if image Nodes have an extra resolution folder
        # if it has it, expand it to get the final TCI image
        for node in response['result']:
            if node['Name'] == 'R10m':
                self.request += f"(R60m)/Nodes"
                response = self.__api_manager.make_request(self.request,
                                                        params={})
                response = response.json()
                break
        
        # Get the final TCI image, if it ends in 10m, it is a 10m image
        for node in response['result']:
            if 'TCI' in  node['Name']:
                self.request += f"({node['Name']})/$value"

                if node['Name'][-7:] == "10m.jp2":
                    print('10m photo')
                    self.__is_image_10m = True

                else: 
                    print('Not 10m photo')
                    self.__is_image_10m = False

                break


    
    def download_image(self, block_size=1024):
        """
        Downloads the image from the Copernicus API and returns a generator
        with the image data, yielding it in blocks of block_size bytes.

        Parameters
        ----------
        block_size : int, optional
            Size of the blocks to yield, by default 1024

        Returns
        -------
        generator
            Generator with the image data
        """

        image_stream, total_size = self.__api_manager.get_image(self.request)
        block_size = 1024

        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            for data in image_stream.iter_content(block_size):
                progress_bar.update(len(data))
                yield data

        

    def __str__(self):
        return self.request