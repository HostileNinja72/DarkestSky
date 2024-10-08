# Darkest Sky

This Project represents the convergence of my passion for astronomy with the craft of programming. It servers as a dynamic project where i apply scientific knowledge from astronomy and geography through programming techniques.

My goal is to make **Darkest sky** a platform where astronomy amateurs can meet at a certain stargazing spot, and organize events.

## How does it suggest the best spot ?

This software utilizes a [score system](./src/Processing/ScoreCalculator.py) that take into consideration, **light pollution**, **clouds**, **moon phase/brightness**... With each variable having its own **weight**. The [**Coordinate generator**](./src/Processing/CoordinateGenerator.py), as it names suggest, generate coordinates for a given radius, under a grid. It calculates the score for each coordinate and then it output the best spot. 
 
> Coordinate generator utilises geospatial computation to generates the coords in a circular area.
### Score 
It is calculated in a straightforward manner, with a linear model. Here are the weights:

```python
WEIGHTS = {
        "light_pollution": 0.3,
        "clouds": 0.2,
        "moon": 0.15,
        "elevation": 0.1,
        "air_quality": 0.1,
        "wind": 0.05,
        "distance": 0.1
    }
```
This score mechanism is ofc subject to change, as there are non-linear effects, and threshhold effects. To change a study must be conducted for precision.


### Light Pollution
The [**light pollution**](./src/DataSource.py) data are from the Word Atlas 2015 dataset provided by the lightpollution api, which provides measurements to estimate light pollution levels.

### Moon data
Moon data are locally calculated in [Moon handler](./src/Processing/MoonHandler.py) from the `de430.bsp` and `naif0012.tls` files.
 - `de430.bsp`:  This file is part of NASA's DE430 ephemeris, which provides high-precision positional data for celestial bodies, including the **Moon**. It allows for accurate computation of the Moon's position in relation to Earth at any given time, which is essential for understanding its impact on observations and measurements.     

 - `naif0012.tls`: This file includes definitions for time systems and reference frames, which are crucial for interpreting the data in SPICE kernels like `de430.bsp`. It ensures that the time and coordinate information used to calculate the Moon's position is correctly aligned with the global reference systems.

These files are read with the help `spiceypy` library.

### Weather
For weather data, We will be using `Visual Crossing Weather API`. It provides most if not all necessary data we need for our project.

## GUI
At first, im developing an admin dashboard to visualize the data and to ease admin control over the software.
We use `PyQt5` with `folium` for this task. The implementation of the GUI is still under development.



