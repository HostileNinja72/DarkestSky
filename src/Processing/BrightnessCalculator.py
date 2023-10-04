import math
from Config.config import NATURAL_BRIGHTNESS

class BrightnessCalculator:

    def __init__(self, data):
        self.data = data

    def compute_brightness_data(self):
        try:
            brightness, elevation = self.data.split(',')
            artif_bright_micro = float(brightness) * 1000
            artif_bright = artif_bright_micro / 1000.0
            total_brightness = artif_bright + NATURAL_BRIGHTNESS
            sqm = math.log10(total_brightness / 108000000) / -0.4
            ratio = artif_bright / NATURAL_BRIGHTNESS
            '''print({
            "Artif. bright.": f"{artif_bright_micro} μcd/m2",
            "Total brightness": f"{total_brightness:.2f} mcd/m2",
            "SQM": f"{sqm:.2f} mag./arc sec2",
            "Ratio": f"{ratio:.2f}",
            "Bortle Class": self.get_bortle(sqm),
            "Elevation": elevation
        })'''
            return sqm
        except ValueError:
            print("Error: Data format is not as expected.")
            return None
        except ZeroDivisionError:
            print("Error: Division by zero encountered.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_bortle(self, sqm_value):
        boundaries = [21.99, 21.89, 21.69, 20.49, 19.50, 18.94, 18.38]
        for i, boundary in enumerate(boundaries, 1):
            if sqm_value > boundary:
                return f"Bortle {i}"
        return "Bortle 9"
