from Processing.CoordinateGenerator import CoordinateGenerator
from pprint import pprint 
from ScoreCache import ScoreCache
from Config.config import LAT, LON, RADIUS

def initialize_system():
    coordinatesGenerator = CoordinateGenerator(10)
    coordinates = coordinatesGenerator.generate_grid_in_circle(LAT, LON, RADIUS)
    scoreCache = ScoreCache(coordinates)
    scoreCache.calculate_and_add_scores_bulk(coordinates)
    return scoreCache

def display_status(scoreCache):
    scoreCache.status()

def get_best_coordinate(scoreCache):
    best_coordinate, best_score = scoreCache.get_best_coordinate()
    pprint((best_coordinate, best_score))




def main():
 
    scoreCache = initialize_system()
    while True:
        choice = input("Enter 1 to see status, Enter 2 to get the best coordinate, 3 to quit: ")

        if choice == '1':
            display_status(scoreCache)
        elif choice == '2':
            get_best_coordinate(scoreCache)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
   
if __name__ == '__main__':
    main()
