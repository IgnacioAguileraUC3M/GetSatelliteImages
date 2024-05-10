


import logging
import requests
import time

from config.request_templates import templates
from src.api_manager import APIManager
from src.SatelliteImage import SatelliteImage

class CopernicusRequest:
    """
    A class used to manage the format of the request to make to the Copernicus
    API, used to add filters and get all the image objects resulting from the
    request, along with filtering and parsing of those images at a root level.


    Attributes
    ----------
    filters : dict
        Dictionary with the filters to add to the request
    request : str
        Request to make to the Copernicus API
    images: list[dict]
        List of dictionaries with the image objects returned by the request (filtered and parsed)


    Methods
    -------
    add_dict_filters(filters: list[dict]) -> None
        Adds a list of filters to the request
    add_filter(type: str, value: str, operand:str, filterOperator:str = "AND", attribute_name: str = None, attribute_type: str = None, polygon_type: str = None) -> None
        Adds a single filter to the request
    get_image_ids(get_all_ids:bool, given_request:str=None, depth:int=0, max_depth:int=5) -> list[dict]
        Uses the APIManager to get the image IDs from the Copernicus API (all of them if specified) and parses them
    parse_image_ids(response: dict) -> list[dict]
        Parse the image IDs from the original data structure to a cleaner one
    """


    def __init__(self, filters: dict = None,
                 get_all_ids = False):

        self.logger = logging.getLogger()   
        self.__request = templates.base_url
        self.__api_manager = APIManager()

        self.__has_filters = False

        self.add_dict_filters(filters) if filters else None
        self.images = self.get_images(get_all_ids=get_all_ids)



    def add_dict_filters(self, filters: list[dict]) -> None:
        """
        Adds a list of filters to the request

        Parameters
        ----------
        filters : list[dict]
            List of dictionaries with the filters to add to the request
        
        Returns
        -------
        None
        """

        _ = {
            'type': 'name',
            'value': 'S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE',
            'operand': '==',
            'filterOperator': 'AND',
            # Attribute specific fields
            'attribute_name': None,
            'attribute_type': None,
            # Polygon specific fields
            'polygon_type': None

        }

        for filter in filters:
            self.add_filter(**filter)



    def add_filter(self, 
                   type: str, 
                   value: str, 
                   operand:str, 
                   filterOperator:str = "AND",
                   attribute_name: str = None,
                   attribute_type: str = None,
                   polygon_type: str = None) -> None:
        """
        Adds a filter to the request

        Parameters
        ----------
        type : str
            Type of filter
                name

                collection

                publication_date

                sensing_date_start

                sensing_date_end

                polygon (needs polygon_type)

                attribute (needs attribute_name and attribute_type)
        value : str
            Value to filter by
        operand : str
            Operand to use in the filter (python syntax)
        filterOperator : str
            Logical operator to use between filters
            Default value: AND
        attribute_name : str
            Name of the attribute to filter by (only used if type is attribute)
            Default value: None
        attribute_type : str
            Type of the attribute (only used if type is attribute)
            Default value: None
        polygon_type : str
            Type of polygon to filter by (only used if type is polygon)
            Default value: None

        """
        
        # If this is the first filter, use the filter template, if not add the
        # specified logial operator
        filter = templates.filter if not self.__has_filters else templates.logical_operators[filterOperator]
        self.__has_filters = True


        # Get the filter type based on the type and format it with the specified values        
        match type.lower():
            case "name":
                filter_type = templates.query_by_name
                operand_value = templates.operands[operand]
                new_filter = filter_type.format(operand=operand_value, 
                                                 value=f"'{value}'"
                                                 )

            case "collection":
                filter_type = templates.query_by_collection
                new_filter = filter_type.format(operand=templates.operands[operand], 
                                                 value=f"'{value}'"
                                                 )

            case "publication_date":
                filter_type = templates.query_by_publication_date
                new_filter = filter_type.format(operand=templates.operands[operand], 
                                                 value=f"{value}"
                                                 )

            case "sensing_date_start":
                filter_type = templates.query_by_sensing_date_start
                new_filter = filter_type.format(operand=templates.operands[operand], 
                                                 value=f"{value}"
                                                 )

            case "sensing_date_end":
                filter_type = templates.query_by_sensing_date_end
                new_filter = filter_type.format(operand=templates.operands[operand], 
                                                 value=f"{value}"
                                                 )

            case "polygon":
                filter_type = templates.query_by_polygon
                new_filter = filter_type.format(value=f"{value}", 
                                                 polygon_type=polygon_type
                                                 )

            case "attribute":
                filter_type = templates.query_by_attribute
                new_filter = filter_type.format(operand=templates.operands[operand],
                                                 value=f"{value}",
                                                 attribute_name=attribute_name,
                                                 type=attribute_type
                                                 )
            
            case _:
                self.logger.error(f"Filter of type \"{type}\" is not supported")
                new_filter = ""


        self.__request += filter + new_filter


    # @property
    # def images(self) -> dict:
    #     return self.get_image_ids(self.request)


    
    def get_images(self,
                      get_all_ids:bool, 
                      given_request:str=None,
                      depth:int=0,
                      max_depth:int=5) -> list[SatelliteImage]:
        """ 
        Get the image IDs from the Copernicus API

        Recucrsively gets the image IDs from the API if the attribute
        get_all_ids is set to True, if not it returns the fist 20 image IDs.
        
        Parameters
        ----------
        request : str
            Request to the Copernicus API
        get_all_ids : bool
            Whether to get all the image IDs
        depth : int
            Depth of the request
        max_depth : int
            Maximum depth of the request
        
        Returns
        -------
        list[dict]
            List containig the imges returned as dictionaries with the image
            attributes 
        """

        # Log the start time if depth is 0
        if depth == 0:
            self.logger.info("Getting image IDs") 
            start_time = time.time()

        # Make the request to the API
        request = given_request if given_request else self.__request
        response_json = self.__api_manager.make_request(request+'&$expand=Attributes')

        # If the response is not 200, log the error and return None
        if response_json.status_code != 200:
            self.logger.error(f"Error: {response_json.status_code}")
            self.logger.error(response_json.text)
            print(str(request))
            return None

        # Parse the response
        response_json = response_json.json()

        # If specified, recursively get next page ids if there are more pages to
        # get and depth is less than max depth 
        if '@odata.nextLink' in response_json and depth < max_depth and get_all_ids:
            next_page_request = response_json['@odata.nextLink']
            next_page_response = self.get_images(get_all_ids=get_all_ids, given_request=next_page_request, depth=depth+1)
            response_json['value'] += next_page_response['value']

        # If depth is 0 all the images have been retrieved
        if depth == 0:
            end_time = time.time()
            total_images_recieved = len(response_json['value'])
            self.logger.info(f"{total_images_recieved} image IDs retrieved in {end_time - start_time} seconds")

            # Parse all the images retrieved 
            response_json = self.parse_image_ids(response_json)

        return response_json



    def parse_image_ids(self, response: dict) -> list[SatelliteImage]:
        """
        Parse image Ids original data structure to a cleaner one

        Transofrms a dictionary with irrelevant information to a list of
        dictionaries with all the image attributes

        Parameters
        ----------
        response : dict
            Original response from the API

        Returns
        -------
        list[dict]
            List containig the imges returned as dictionaries with the image
            attributes

        """

        response_images = response['value']
        parsed_images = [SatelliteImage(*image) for image in response_images]
        
        return parsed_images
    


    @property 
    def __request(self) -> str:
        return self.__request


    def __str__(self):
        return self.__request
    


        