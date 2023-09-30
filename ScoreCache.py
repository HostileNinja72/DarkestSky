from concurrent.futures import ThreadPoolExecutor
import heapq
import time
from Processing.ScoreCalculator import ScoreCalculator

class ScoreCache:
    """A class that caches scores of various coordinates using a hash map and a priority queue.

    The score for each coordinate is computed using a score calculator and is set to expire after an hour.

    Attributes:
        scores (dict): A dictionary holding coordinate-score pairs.
        queue (list): A priority queue to hold coordinates based on their scores and expiry time.
    """

    def __init__(self, initial_coordinates):
        """Initializes the ScoreCache with a set of initial coordinates.

        Args:
            initial_coordinates (iterable): An iterable of coordinates to initialize the cache with.
        """
        self.scores = {coord: None for coord in initial_coordinates}  
        self.queue = [] 

    def _calculate_and_add_score(self, coordinate):
        """Calculates the score for a given coordinate and adds it to the hash map and priority queue.

        The score is calculated using a score calculator. The method also sets the score to expire after one hour.

        Args:
            coordinate (tuple): The coordinate to calculate the score for.
        """
        if coordinate in self.scores:
            try:
                score = ScoreCalculator().compute_score(coordinate)
                expiry_time = time.time() + 3600  # Score is valid for one hour

                # Update hash map
                self.scores[coordinate] = score

                # Add to priority queue
                heapq.heappush(self.queue, (-score, expiry_time, coordinate))
            except Exception as e:
                print(f"Failed to calculate score for {coordinate}. Error: {e}")

    def get_best_coordinate(self):
        """Gets the best coordinate from the priority queue based on the highest score and validity.

        Returns:
            tuple: The coordinate with the highest score and its score, or (None, None) if no valid coordinate is found.
        """
        while self.queue:
            negative_score, expiry_time, coordinate = heapq.heappop(self.queue)  
            if expiry_time > time.time():  # If not expired
                return coordinate, -negative_score
        return None, None

    def get_score(self, coordinate):
        """Gets the score for a given coordinate from the hash map.

        Args:
            coordinate (tuple): The coordinate to get the score for.

        Returns:
            int: The score of the coordinate, or None if not found.
        """
        return self.scores.get(coordinate)

    def calculate_and_add_scores_bulk(self, coordinates):
        """Calculates and adds scores for a bulk of coordinates using a ThreadPoolExecutor.

        Args:
            coordinates (iterable): An iterable of coordinates to calculate and add scores for.
        """
        with ThreadPoolExecutor() as executor:
            executor.map(self._calculate_and_add_score, coordinates)

    def status(self):
        """Prints the status of the priority queue, including details of each coordinate, its score, and expiry status.

        This method also provides statistics on the total number of coordinates, the number with calculated scores, and the number of expired scores.
        """
        print("\nPriority Queue (from highest to lowest score):")
        temp_queue = sorted(self.queue, key=lambda x: (x[0], x[1]))  
        for negative_score, expiry_time, coordinate in temp_queue:
            remaining_time = expiry_time - time.time()
            if remaining_time < 0:
                expiry_time_str = "Expired"
            else:
                expiry_time_str = f"Expires in {int(remaining_time)} seconds"
            print(f"Coordinate: {coordinate}, Score: {-negative_score}, {expiry_time_str}")

        num_coordinates_with_scores = sum(1 for score, _, _ in temp_queue if score is not None)

        print(f"\nTotal Coordinates: {len(temp_queue)}")
        print(f"Coordinates with Scores: {num_coordinates_with_scores}")
        print(f"Expired Coordinates: {len(temp_queue) - num_coordinates_with_scores}")
