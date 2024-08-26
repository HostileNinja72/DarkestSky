import random
import requests 
from Processing.BrightnessCalculator import BrightnessCalculator
from Processing.MoonHandler import MoonHandler
from Config.config import LIGHT_POLLUTION_KEY as key_lp
from datetime import datetime

class DataSource:

    def __init__(self):
        self.noform_time = datetime.now()
        self.time = self.noform_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_light_pollution(self, coordinate):
        lat, long = coordinate
        url = "https://www.lightpollutionmap.info/QueryRaster/"
        query_params = {
            "key": key_lp,  
            "ql": "wa_2015",      
            "qt": "point",       
            "qd": f"{long},{lat}" 
        }
        try:
            response = requests.get(url, params=query_params)
            response.raise_for_status()  
            if(response.text == "Daily quota exceeded"):
                print("Daily quota exceeded, no light pollution data ;(")
                exit(1)
            return BrightnessCalculator(response.text).compute_brightness_data()
        except requests.RequestException as e:
            print(f"Error fetching light pollution data: {e}")
            return None

    def get_clouds(self, coordinate):
        return random.uniform(0, 100)

    def get_moon_brightness(self):
        return  random.uniform(0, 100)

    def get_elevation(self, coordinate):
        return random.uniform(0, 5000)

    def get_air_quality(self, coordinate):
        # Random Air Quality Index (AQI) value between 0 (excellent air quality) and 500 (hazardous)
        return random.uniform(0, 500)

    def get_wind(self, coordinate):
        # Random wind speed between 0 and 50 km/h
        return random.uniform(0, 50)

    def get_distance(self, coordinate):
        # Random distance value between 0 and 500 km
        return random.uniform(0, 500)

if __name__ == "__main__":
    ds = DataSource()
    print(ds.get_light_pollution((33.53210, -5.10950)))