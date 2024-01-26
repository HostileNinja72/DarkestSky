from concurrent.futures import ThreadPoolExecutor
import heapq
import time
from Processing.ScoreCalculator import ScoreCalculator
import curses

class ScoreCache:

    def __init__(self, initial_coordinates):
        self.scores = {coord: None for coord in initial_coordinates}  
        self.queue = []
        self.score_calculator = ScoreCalculator()  

    def _calculate_and_add_score(self, coordinate):
        if coordinate in self.scores:
            try:
                score = self.score_calculator.compute_score(coordinate)
                expiry_time = time.time() + 3600

                self.scores[coordinate] = score
                heapq.heappush(self.queue, (-score, expiry_time, coordinate))
            except Exception as e:
                print(f"Failed to calculate score for {coordinate}. Error: {e}")
                exit(1)

    def _peek(self, heap):
        """Peek at the top item of the heap without popping it."""
        return heap[0] if heap else None

    def get_best_coordinate(self):
        while self.queue:
            top_item = self._peek(self.queue)
            _, expiry_time, _ = top_item
            if expiry_time <= time.time():  # If expired
                heapq.heappop(self.queue)
            else:
                negative_score, _, coordinate = top_item  # Use the peeked item
                return coordinate, -negative_score
        return None, None


    def get_score(self, coordinate):
        return self.scores.get(coordinate)

    def calculate_and_add_scores_bulk(self, coordinates):
        with ThreadPoolExecutor() as executor:
            # Using list comprehension to force waiting for completion
            list(executor.map(self._calculate_and_add_score, coordinates))
    
    def _render_status(self, stdscr):
        curses.curs_set(0)  # Hide cursor

        # Starting offset for the list
        offset = 0

        while True:
            stdscr.clear()

            height, width = stdscr.getmaxyx()

        
            stdscr.addstr(0, 0, "Priority Queue (from highest to lowest score):", curses.A_BOLD)

            stdscr.addstr(2, 0, "Coordinate", curses.A_UNDERLINE)
            stdscr.addstr(2, 40, "Score", curses.A_UNDERLINE)
            stdscr.addstr(2, 60, "Status", curses.A_UNDERLINE)

            temp_queue = sorted(self.queue, key=lambda x: (x[0], x[1]))

            max_items = height - 4

            for idx, (negative_score, expiry_time, coordinate) in enumerate(temp_queue[offset:offset+max_items], start=3):
                remaining_time = expiry_time - time.time()
                expiry_time_str = "Expired" if remaining_time < 0 else f"Expires in {int(remaining_time)}s"
                stdscr.addstr(idx, 0, str(coordinate))
                stdscr.addstr(idx, 40, str(-negative_score))
                stdscr.addstr(idx, 60, expiry_time_str)

          
            if len(temp_queue) > offset + max_items:
                stdscr.addstr(height - 1, 0, "...Press DOWN for more items...", curses.A_BOLD)
            elif offset > 0:
                stdscr.addstr(height - 1, 0, "...Press UP for previous items...", curses.A_BOLD)

            key = stdscr.getch()
            if key == curses.KEY_DOWN and len(temp_queue) > offset + max_items:
                offset += 1
            elif key == curses.KEY_UP and offset > 0:
                offset -= 1
            elif key == ord('q'):
                break


    def status(self):
        curses.wrapper(self._render_status)

