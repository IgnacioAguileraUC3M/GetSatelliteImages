
# from src.copernicus_request import CopernicusRequest
from src.ImageRequest import ImageRequest
from src.APIManager import APIManager 
from src.GeoPolygon import GeoPolygon

class SatelliteImage:
    """
    A class to manage all the information of a satellite image. Also includes
    the logic to download the image from the Copernicus API.

    Attributes
    ----------
    api_manager : APIManager
        APIManager object to make the requests
    image_path : str 
        Path to save the image
        Default value: 'tmp/test.jp2'
    kwargs : dict
        Dictionary with the image attributes straight from the API

    Methods
    -------
    get_image_url()
        Gets the image URL from the API, aka instanciates the ImageRequest object
    download(block_size=1024, image_path=None)
        Downloads the image from the API and saves it in the specified path
    parse_kwargs(kwargs)
        Parses the attributes from the API to the class attributes
    get_geo_footprint(geofootprint)
        Gets the coordinates of the image footprint
    unwrap_attributes(attributes)
        Unwraps the attributes from the API to the class attributes
    """


    def __init__(self, 
                 api_manager:APIManager = None, 
                 image_path:str = 'tmp/test.jp2',
                 **kwargs) -> None:

        self.parse_kwargs(kwargs)
        self.api_manager = APIManager() if not api_manager else api_manager
        self.image_path = image_path
        self.image_request = None


    def get_image_url(self):
        """
        Instanciates the ImageRequest object to get the image URL

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.image_request = ImageRequest(self.id, self.api_manager)


    def download(self, block_size:int=1024, image_path:str=None):
        """
        Downloads the image from the API and saves it in the specified path

        Parameters
        ----------
        block_size : int, optional
            Size of the blocks to download the image, by default 1024
        image_path : str, optional
            Path to save the image, by default None

        Returns
        -------
        None
        """

        if not self.image_request: 
            print("No image request found, getting image request")
            self.get_image_url()

        image_path = image_path if image_path else self.image_path

        image_data_iterator = self.api_manager.get_image_stream(self.image_request.request, 
                                                                block_size=block_size)
        with open(image_path, "wb") as image_file:
            for data in image_data_iterator:
                image_file.write(data)



    def parse_kwargs(self, kwargs:dict):
        """
        Parses the attributes from the API to the class attributes

        Parameters
        ----------
        kwargs : dict
            Dictionary with the image attributes straight from the API

        Returns
        -------
        None
        """

        self.id                 = kwargs.get("Id", None)
        self.name               = kwargs.get("Name", None)
        self.contentType        = kwargs.get("ContentType", None)
        self.contentLength      = kwargs.get("ContentLength", None)
        self.originDate         = kwargs.get("OriginDate", None)
        self.publicationDate    = kwargs.get("PublicationDate", None)
        self.modificationDate   = kwargs.get("ModificationDate", None)
        self.online             = kwargs.get("Online", None)
        self.geofootprint       = self.get_geo_footprint(kwargs.get("GeoFootprint", None))
        self.polygon            = GeoPolygon(self.geofootprint) if self.geofootprint else None

        self.unwrap_attributes(kwargs.get("Attributes", None))



    def get_geo_footprint(self, geofootprint:dict=None):
        """
        Gets the coordinates of the image footprint

        Parameters
        ----------
        geofootprint : dict, optional
            Dictionary with the image footprint coordinates

        Returns
        -------
        list
            List with the coordinates of the image footprint
        """

        if not geofootprint: return None
        coordinates = geofootprint.get("coordinates", None)
        if not coordinates: return None
        return coordinates[0]        
    


    def unwrap_attributes(self, attributes:dict=None):
        """
        Unwraps the attributes from the API to the class attributes

        Parameters
        ----------
        attributes : dict, optional
            Dictionary with the image attributes

        Returns
        -------
        None
        """

        if not attributes: return None

        for attribute in attributes:
            match attribute["Name"]:
                case "origin":
                    self.origin = attribute["Value"]

                case "tileId":
                    self.tileId = attribute["Value"]

                case "cloudCover":
                    self.cloudCover = attribute["Value"]

                case "datastripId":
                    self.datastripId = attribute["Value"]

                case "orbitNumber":
                    self.orbitNumber = attribute["Value"]

                case "sourceProduct":
                    self.sourceProduct = attribute["Value"]

                case "processingDate":
                    self.processingDate = attribute["Value"]

                case "productGroupId":
                    self.productGroupId = attribute["Value"]

                case "operationalMode":
                    self.operationalMode = attribute["Value"]

                case "processingLevel":
                    self.processingLevel = attribute["Value"]

                case "processorVersion":
                    self.processorVersion = attribute["Value"]

                case "granuleIdentifier":
                    self.granuleIdentifier = attribute["Value"]

                case "platformShortName":
                    self.platformShortName = attribute["Value"]

                case "instrumentShortName":
                    self.instrumentShortName = attribute["Value"]

                case "relativeOrbitNumber":
                    self.relativeOrbitNumber = attribute["Value"]

                case "sourceProductOriginDate":
                    self.sourceProductOriginDate = attribute["Value"]

                case "platformSerialIdentifier":
                    self.platformSerialIdentifier = attribute["Value"]

                case "productType":
                    self.productType = attribute["Value"]

                case "beginningDateTime":
                    self.beginningDateTime = attribute["Value"]

                case "endingDateTime":
                    self.endingDateTime = attribute["Value"]













############################################################################3
############################################################################3
############################################################################3

    # def __init__(self, 
    #              image_path: str, 
    #              filters: dict = None,
    #              image_selection_strategy: str = "latest"):

        # self.image_path = image_path
        # self.image_selection_strategy = image_selection_strategy
        # self.image_path = './tmp/test.jp2'
        # self.block_size = 1024

        # self.coprernicus_request = CopernicusRequest(filters)
        # self.image_request = self.select_image()


    # def select_image(self):

    #     selected_image = self.image_selection()
    #     image_request = ImageRequest(selected_image["Id"])
    #     return image_request
        



    # def image_selection(self):
    #     """
    #     Image selection strategies:
    #         - latest
    #         - has specified coordinate most centered
    #         - Lowest cloud coverage
    #         - Clesest to specified date
    #         - Contiains specified attribute
    #         - Contains specified polygon


    #     Currently this method gets all the retrieved images and selects one following the next criteria:
    #         - The image is a square (4 coordinates in the polygon)
    #         - The image has the lowest cloud coverage
    #         - If none of the images are squares it selects the one with the lowest cloud coverage


    #     TODO: 
    #         - Implement the rest of the selection strategies
    #         - Figure out how to filter by image resolution
    #         - Implement the selection strategy as a parameter
    #         - Stablish the selection strategy pipeline

    #     """

    #     all_images = self.coprernicus_request.images
    #     discarded_images = []
    #     accepted_images = []

    #     for image in all_images:
    #         image_footprint = image["GeoFootprint"]["coordinates"][0]
    #         hascloudcover = False
    #         for attribute in image["Attributes"]:
    #             if attribute['Name'] == "cloudCover": image_cloud_coverage = attribute['Value']; hascloudcover = True

    #         if not hascloudcover: image_cloud_coverage = 100.00

    #         image["cloudCover"] = image_cloud_coverage
                
    #         # image_cloud_coverage 

    #         if len(image_footprint) == 5: accepted_images.append(image)
    #         else: discarded_images.append(image) # Skip if the image is not a square

    #     if len(accepted_images) == 0:
    #         accepted_images = discarded_images            

    #     accepted_images.sort(key=lambda image: image["cloudCover"]) # Sort by cloud coverage

    #     return accepted_images[0]



    # def download(self):
    #     image_data_iterator = self.image_request.download_image(self.block_size)
    #     with open(self.image_path, "wb") as image_file:
    #         for data in image_data_iterator:
    #             image_file.write(data)