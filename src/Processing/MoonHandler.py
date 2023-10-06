import spiceypy as spice
import numpy as np
import math

spice.furnsh('../resources/naif0012.tls')  # Load the leap seconds kernel
spice.furnsh('../resources/de430.bsp')  # Load the ephemeris file


class MoonHandler:
    def __init__(self, time):
        self.time = time
        et = spice.str2et(time)
        self.pos_moon, _ = spice.spkpos('MOON', et, 'J2000', 'NONE', 'EARTH')
        self.pos_sun, _ = spice.spkpos('SUN', et, 'J2000', 'NONE', 'EARTH')

    @staticmethod
    def calculate_RA_vector(pos):
        x, y, _ = pos
        RA = math.degrees(math.atan2(y, x))
        return RA
    
    def calculate_distance(self):
        return np.linalg.norm(self.pos_moon)

    def phase(self):
        RA_moon = MoonHandler.calculate_RA_vector(self.pos_moon)
        RA_sun = MoonHandler.calculate_RA_vector(self.pos_sun)

        O = math.acos(
            np.dot(self.pos_moon, self.pos_sun) /
            (np.linalg.norm(self.pos_moon[:2]) * np.linalg.norm(self.pos_sun[:2]))
        )
        O_degrees = math.degrees(O)
        
        if RA_moon < RA_sun:
            O_degrees = -O_degrees
        
        return O_degrees
    def brightness(self):
        return ((abs(self.phase())/180)*(pow(self.calculate_distance()/356500,2)))/1.3

    

    





"""time = "2023-10-24 20:30:00"
moon_handler = MoonHandler(time)
print(f"Distance from Earth to Moon: {moon_handler.calculate_distance():.2f} km")
print(f"Phase: {moon_handler.phase():.2f} degrees")"""



