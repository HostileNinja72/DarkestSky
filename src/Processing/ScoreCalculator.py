from Config.config import RADIUS
from DataSource import DataSource

class ScoreCalculator:

    # Weight definitions
    WEIGHTS = {
        "light_pollution": 0.3,
        "clouds": 0.2,
        "moon": 0.15,
        "elevation": 0.1,
        "visibility": 0.1,
        "wind": 0.05,
        "distance": 0.1
    }

    def __init__(self):
        # Assuming a data source or API which provides the values for each factor
        self.data_source = DataSource()
    
    def normalize(self, value, max_value, min_value=0, reverse=False):
        normalized = (value - min_value) / (max_value - min_value)
        return 1 - normalized if reverse else normalized

    def compute_score(self, coordinate):

        # Fetch or compute values for each factor using the data_source
        light_pollution = self.data_source.get_light_pollution(coordinate)
        clouds = self.data_source.get_clouds(coordinate)
        moon = self.data_source.get_moon_brightness()
        elevation = self.data_source.get_elevation(coordinate)
        visibility = self.data_source.get_visibility(coordinate)
        wind = self.data_source.get_wind(coordinate)
        distance = self.data_source.get_distance(coordinate)

        # Normalize each valuecls
        
        scores = {
            "light_pollution": self.normalize(light_pollution, max_value=25, min_value = 15, reverse=True),
            "clouds": self.normalize(clouds, max_value=100, reverse=True),
            "moon": self.normalize(moon, max_value=1, reverse=True),
            "elevation": self.normalize(elevation, max_value=3000),  # assuming max elevation of 5000 meters
            "visibility": self.normalize(visibility, max_value=15), 
            "wind": self.normalize(wind, max_value=50, reverse=True),  # assuming max wind speed of 50 km/h
            "distance": self.normalize(distance, max_value=RADIUS, reverse=True)  # assuming max distance of 500 km
        }

        # Calculate the composite score
        composite_score = sum([scores[factor] * weight for factor, weight in self.WEIGHTS.items()])
        
        return composite_score
