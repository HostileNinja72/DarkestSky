import os
import sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

from flask import Flask, request, jsonify
from Processing.CoordinateGenerator import CoordinateGenerator
from ScoreCache import ScoreCache
from Config.config import RADIUS

app = Flask(__name__)
scoreCache = None  # Initialize the global variable to None

AVAILABLE_ACTIONS = ["best"]

def initialize_system(LAT, LON):
    coordinatesGenerator = CoordinateGenerator(10)
    coordinates = coordinatesGenerator.generate_grid_in_circle(LAT, LON, RADIUS)
    scoreCache = ScoreCache(coordinates)
    scoreCache.calculate_and_add_scores_bulk(coordinates)
    return scoreCache

def get_best_coordinate(scoreCache):
    best_coordinate, best_score = scoreCache.get_best_coordinate()
    return best_coordinate, best_score

@app.route('/perform_action', methods=['POST'])
def perform_action():
    global scoreCache  # Declare global variable to modify it
    data = request.get_json()  
    lat = data.get('lat')
    lon = data.get('lon')
    action = data.get('action')

    if lat is None or lon is None or action is None:
        return jsonify({'error': 'Missing parameters', "lat": lat, "lon": lon}), 400

    # Initialize the system only if it hasn't been initialized yet
    if scoreCache is None:
        scoreCache = initialize_system(lat, lon)

    if action not in AVAILABLE_ACTIONS:
        return jsonify({
            "error": f"The action '{action}' does not exist",
            "available_actions": AVAILABLE_ACTIONS
        }), 400

    if action == "best":
        best, _ = get_best_coordinate(scoreCache)
        return jsonify({'lat': best[0], 'long': best[1]})

    # ... additional actions can be handled here

if __name__ == '__main__':
    app.run(debug=True)