import spiceypy as spice
import numpy as np
import math
import os

resource_path = '/app/resources/'

spice.furnsh(os.path.join(resource_path, 'naif0012.tls'))  
spice.furnsh(os.path.join(resource_path, 'de430.bsp')) 

class MoonHandler():
    @staticmethod
    def calculate_positions(time):
        et = spice.str2et(time)
        pos_moon, _ = spice.spkpos('MOON', et, 'J2000', 'NONE', 'EARTH')
        pos_sun, _ = spice.spkpos('SUN', et, 'J2000', 'NONE', 'EARTH')
        return pos_moon, pos_sun

    @staticmethod
    def calculate_RA_vector(pos):
        x, y, _ = pos
        RA = math.degrees(math.atan2(y, x))
        return RA

    @staticmethod
    def calculate_distance(pos_moon):
        return np.linalg.norm(pos_moon)

    @staticmethod
    def phase(pos_moon, pos_sun):
        RA_moon = MoonHandler.calculate_RA_vector(pos_moon)
        RA_sun = MoonHandler.calculate_RA_vector(pos_sun)

        O = math.acos(
            np.dot(pos_moon, pos_sun) /
            (np.linalg.norm(pos_moon[:2]) * np.linalg.norm(pos_sun[:2]))
        )
        O_degrees = math.degrees(O)

        if RA_moon < RA_sun:
            O_degrees = -O_degrees
        return O_degrees

    @staticmethod
    def brightness(phase, distance):
        return ((abs(phase)/180)*(pow(distance/356500,2)))/1.3

class ObserverMoon:

    def calculate_moonrise(time, observer_coordinates):
        # Calculation code here
        pass

    def calculate_moonset(time, observer_coordinates):
        pass
