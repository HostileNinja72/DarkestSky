from concurrent.futures import ThreadPoolExecutor
import heapq
import time
import redis
import json
from Processing.ScoreCalculator import ScoreCalculator
import curses
import os

class ScoreCache:

    def __init__(self, initial_coordinates):
        self.redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=os.getenv('REDIS_PORT', 6379))
        self.score_calculator = ScoreCalculator()

        for coord in initial_coordinates:
            if not self.redis_client.exists(f"score:{coord}"):
                self.redis_client.set(f"score:{coord}", json.dumps({"score": None, "expiry_time": None}))

    def _calculate_and_add_score(self, coordinate):
        try:
            score = self.score_calculator.compute_score(coordinate)
            expiry_time = time.time() + 3600

            
            self.redis_client.set(f"score:{coordinate}", json.dumps({"score": score, "expiry_time": expiry_time}))
            
            self.redis_client.zadd("queue", {json.dumps({"coordinate": coordinate, "score": score, "expiry_time": expiry_time}): -score})
        except Exception as e:
            print(f"Failed to calculate score for {coordinate}. Error: {e}")
            exit(1)

    def _peek(self):
        """Peek at the top item of the priority queue in Redis without popping it."""
        top_item = self.redis_client.zrange("queue", 0, 0)
        if top_item:
            return json.loads(top_item[0])
        return None

    def get_best_coordinate(self):
        while True:
            top_item = self._peek()
            if not top_item:
                return None, None

            expiry_time = top_item["expiry_time"]
            if expiry_time <= time.time():  # If expired
                self.redis_client.zrem("queue", json.dumps(top_item))
            else:
                return top_item["coordinate"], top_item["score"]

    def get_score(self, coordinate):
        score_data = self.redis_client.get(f"score:{coordinate}")
        if score_data:
            return json.loads(score_data)["score"]
        return None

    def calculate_and_add_scores_bulk(self, coordinates):
        with ThreadPoolExecutor() as executor:
            list(executor.map(self._calculate_and_add_score, coordinates))

    def _render_status(self, stdscr):
        curses.curs_set(0)  # Hide cursor
        offset = 0

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            stdscr.addstr(0, 0, "Priority Queue (from highest to lowest score):", curses.A_BOLD)
            stdscr.addstr(2, 0, "Coordinate", curses.A_UNDERLINE)
            stdscr.addstr(2, 40, "Score", curses.A_UNDERLINE)
            stdscr.addstr(2, 60, "Status", curses.A_UNDERLINE)

            queue_items = self.redis_client.zrange("queue", offset, offset + height - 4, withscores=True)
            if not queue_items:
                stdscr.addstr(3, 0, "No items in the queue.")
            else:
                for idx, (item, _) in enumerate(queue_items, start=3):
                    data = json.loads(item)
                    remaining_time = data["expiry_time"] - time.time()
                    expiry_time_str = "Expired" if remaining_time < 0 else f"Expires in {int(remaining_time)}s"
                    stdscr.addstr(idx, 0, str(data["coordinate"]))
                    stdscr.addstr(idx, 40, str(data["score"]))
                    stdscr.addstr(idx, 60, expiry_time_str)

            if len(queue_items) >= height - 4:
                stdscr.addstr(height - 1, 0, "...Press DOWN for more items...", curses.A_BOLD)
            elif offset > 0:
                stdscr.addstr(height - 1, 0, "...Press UP for previous items...", curses.A_BOLD)

            key = stdscr.getch()
            if key == curses.KEY_DOWN and len(queue_items) >= height - 4:
                offset += 1
            elif key == curses.KEY_UP and offset > 0:
                offset -= 1
            elif key == ord('q'):
                break

    def status(self):
        curses.wrapper(self._render_status)
