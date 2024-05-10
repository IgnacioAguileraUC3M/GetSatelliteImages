from src.copernicus_request import CopernicusRequest 
from src.image_request import ImageRequest
from src.token_manager import TokenManager
from src.api_manager import APIManager
from src.polygon_manager import CopernicusPolygon
from utils.setup_logger import setup_logging
from src.SatelliteImage import SatelliteImage

import time
import logging
import json
import hashlib
from tqdm import tqdm

test_request_filters = [
    # {
    #     'type': 'name',
    #     'value': 'S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE',
    #     'operand': '==',
    #     'filterOperator': 'AND',
    #     'attribute_name': None,
    #     'attribute_type': None
    # },
    {
        'type': 'sensing_date_start',
        'value': '2023-02-03T00:00:00.000Z',
        'operand': '>',
        'filterOperator': 'AND',
        'attribute_name': None,
        'attribute_type': None
    },
    {
        'type': 'collection',
        'value': 'SENTINEL-2',
        'operand': '==',
        'filterOperator': 'AND',
        'attribute_name': None, 
        'attribute_type': None
    },
    {
        'type': 'polygon',
        'value': '-3.681883 40.245938',
        'operand': None,
        'polygon_type': 'POINT',
        'filterOperator': 'AND'

    },
    {
        'type': 'attribute',
        'value': '10.00',
        'operand': '<=',
        'filterOperator': 'AND',
        'attribute_name': 'cloudCover',
        'attribute_type': 'Double'
    }
]


def main():

    image = SatelliteImage("./tmp/test.jp2", test_request_filters)
    image.download()

    exit()
    logger = logging.getLogger()
    setup_logging()
    logger.info("Starting the application")

    request = CopernicusRequest(test_request_filters, get_all_ids=False)
    import random
    import json

    

    image = random.choice(request.images)
    with open("image.json", "w") as file:
        file.write(json.dumps(image, indent=4))
    
    image_request = ImageRequest(image['Id'], api_manager=APIManager())
    print(image_request)
    exit()
    print(request)
    api = APIManager()
    images = api.get_image_ids(request, get_all_ids=False)



    for image in images['value']:
        footprint_str = image['Footprint'].split('POLYGON')[1].strip().replace("'", "").replace("(", "").replace(")", "")
        polygon = []

        for coordinate in footprint_str.split(","):
            lat, lon = coordinate.strip().split(" ")
            polygon.append([float(lon), float(lat)])

        image_polygon = CopernicusPolygon(polygon)

        # if image_polygon.area < 1: continue

        image_request = ImageRequest(image['Id'], api_manager=api)
        # if not image_request.is_image_10m:
        #     continue


        image_stream, total_size = api.get_image(image_request)
        block_size = 1024

        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open("producttest.jp2", "wb") as file:
                for data in image_stream.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        exit()


        


if __name__ == "__main__":
    main()  