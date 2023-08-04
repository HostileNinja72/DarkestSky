import math
from Config.config import RADIUS

class CoordinateGenerator: 
    GRID_SIZE = 10
    EARTH_RADIUS = 6371.0 
    number_of_coord = 0

    def __init__(self, GRID_SIZE):
        self.GRID_SIZE = GRID_SIZE
        pass

    def _new_coords_from_displacement(self, lat, long, dy, dx):
        """Return new coordinates after moving dy km north and dx km east."""
        delta_lat = (dy / self.EARTH_RADIUS) * (180 / math.pi)
        delta_long = (dx / self.EARTH_RADIUS) * (180 / math.pi) / math.cos(math.radians(lat))

        new_lat = lat + delta_lat
        new_long = long + delta_long

        return new_lat, new_long

    def _haversine_distance(self, coord1, coord2):
        lat1, long1 = coord1
        lat2, long2 = coord2
        d_lat = math.radians(lat2 - lat1)
        d_long = math.radians(long2 - long1)
        a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_long/2)**2
        return 2 * self.EARTH_RADIUS * math.asin(math.sqrt(a))

    def generate_grid_in_circle(self, center_lat, center_long, radius_km=RADIUS):  # public method
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
        return self.number_of_coord
