import math
from Config.config import RADIUS

class CoordinateGenerator:
    """A class to generate a grid of coordinates within a circle.
    
    Attributes:
        GRID_SIZE (int): The distance between adjacent points in the grid. Defaults to 10.
        EARTH_RADIUS (float): The radius of the Earth in kilometers. Defaults to 6371.0 km.
        number_of_coord (int): Stores the number of coordinates generated in the last grid generation operation.
    """
    
    GRID_SIZE = 10
    EARTH_RADIUS = 6371.0
    number_of_coord = 0

    def __init__(self, GRID_SIZE):
        """Initializes the CoordinateGenerator with a specified grid size.

        Args:
            GRID_SIZE (int): The distance between adjacent points in the grid.
        """
        self.GRID_SIZE = GRID_SIZE

    def _new_coords_from_displacement(self, lat, long, dy, dx):
        """Private method to return new coordinates after moving a specified distance to the north and east from the initial coordinates.

        Args:
            lat (float): The initial latitude in degrees.
            long (float): The initial longitude in degrees.
            dy (float): The displacement in the north direction in kilometers.
            dx (float): The displacement in the east direction in kilometers.

        Returns:
            tuple: A tuple containing the new latitude and longitude in degrees.
        """
        delta_lat = (dy / self.EARTH_RADIUS) * (180 / math.pi)
        delta_long = (dx / self.EARTH_RADIUS) * (180 / math.pi) / math.cos(math.radians(lat))

        new_lat = lat + delta_lat
        new_long = long + delta_long

        return new_lat, new_long

    def _haversine_distance(self, coord1, coord2):
        """Private method to calculate the haversine distance between two coordinates.

        Args:
            coord1 (tuple): A tuple containing the latitude and longitude of the first coordinate in degrees.
            coord2 (tuple): A tuple containing the latitude and longitude of the second coordinate in degrees.

        Returns:
            float: The haversine distance between the two coordinates in kilometers.
        """
        lat1, long1 = coord1
        lat2, long2 = coord2
        d_lat = math.radians(lat2 - lat1)
        d_long = math.radians(long2 - long1)
        a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_long/2)**2
        return 2 * self.EARTH_RADIUS * math.asin(math.sqrt(a))

    def generate_grid_in_circle(self, center_lat, center_long, radius_km=RADIUS):
        """Generates a grid of coordinates inside a circle defined by its center and radius.

        Args:
            center_lat (float): The latitude of the circle's center in degrees.
            center_long (float): The longitude of the circle's center in degrees.
            radius_km (float): The radius of the circle in kilometers. Defaults to the value of RADIUS from the Config module.

        Returns:
            list: A list of tuples where each tuple contains the latitude and longitude of a point in the grid that lies within the circle.
        """
        lat_steps = int(2 * radius_km / self.GRID_SIZE) + 1
        long_steps = int(2 * radius_km / self.GRID_SIZE) + 1

        top_left_lat, top_left_long = self._new_coords_from_displacement(center_lat, center_long, radius_km, -radius_km)

        grid = []

        for lat_step in range(lat_steps):
            for long_step in range(long_steps):
                current_lat, current_long = self._new_coords_from_displacement(top_left_lat, top_left_long, -lat_step * self.GRID_SIZE, long_step * self.GRID_SIZE)

                if self._haversine_distance((center_lat, center_long), (current_lat, current_long)) <= radius_km:
                    grid.append((current_lat, current_long))
        self.number_of_coord = len(grid)
        return grid

    def get_number_of_coords(self):
        """Returns the number of coordinates generated in the last grid generation operation.

        Returns:
            int: The number of coordinates generated.
        """
        return self.number_of_coord
