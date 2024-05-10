
# from src.copernicus_request import CopernicusRequest
# from src.image_request import ImageRequest


class SatelliteImage:

    def __init__(self) -> None:
        pass













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