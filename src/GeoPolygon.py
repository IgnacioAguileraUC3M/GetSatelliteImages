
from shapely.geometry import Polygon    # Probbaly will be used in the future


class GeoPolygon():

    def __init__(self, coordinates: list[tuple[float]]):

        self.polygon = Polygon(coordinates)
        self.coordinates = coordinates
        self.area = self.polygon.area

        
