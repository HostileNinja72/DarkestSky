from concurrent.futures import ThreadPoolExecutor
import heapq
import time
from Processing.ScoreCalculator import ScoreCalculator

class ScoreCache:
    def __init__(self, initial_coordinates):
        self.scores = {coord: None for coord in initial_coordinates}  
        self.queue = []  # Priority Queue: [(-score, expiry_time, coordinate)]

    def _calculate_and_add_score(self, coordinate):
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
        # This loop ensures expired coordinates are removed and finds the best coordinate
        while self.queue:
            negative_score, expiry_time, coordinate = heapq.heappop(self.queue)  
            if expiry_time > time.time():  # If not expired
                return coordinate, -negative_score  # Returning the coordinate and its score
        return None, None  # No best coordinate found

    def get_score(self, coordinate):
        return self.scores.get(coordinate)
      
    def calculate_and_add_scores_bulk(self, coordinates):
        with ThreadPoolExecutor() as executor:
            executor.map(self._calculate_and_add_score, coordinates)

    def status(self):
        # Print the priority queue
        print("\nPriority Queue (from highest to lowest score):")
        temp_queue = sorted(self.queue, key=lambda x: (x[0], x[1]))  # Sorting by score first, then expiry
        for negative_score, expiry_time, coordinate in temp_queue:
            remaining_time = expiry_time - time.time()
            if remaining_time < 0:
                expiry_time_str = "Expired"
            else:
                expiry_time_str = f"Expires in {int(remaining_time)} seconds"
            print(f"Coordinate: {coordinate}, Score: {-negative_score}, {expiry_time_str}")

        # Print additional information
        #num_coordinates_with_scores = sum(1 for _, score in self.scores.items() if score is not None)
        num_coordinates_with_scores = sum(1 for score, _, _ in temp_queue if score is not None)

        print(f"\nTotal Coordinates: {len(temp_queue)}")
        print(f"Coordinates with Scores: {num_coordinates_with_scores}")
        print(f"Expired Coordinates: {len(temp_queue) - num_coordinates_with_scores}")
