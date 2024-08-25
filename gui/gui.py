import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import geemap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Earth Engine with PyQt5")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a QWebEngineView
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Create a map using geemap
        self.map_widget = geemap.Map()
        self.map_widget.add_basemap('HYBRID')

        # Example coordinates (ensure these are valid)
        lat, lon = 31.16580958786196, -7.9375  # Replace with your actual coordinates

        # Debugging: Print the coordinates
        print(f"Latitude: {lat}, Longitude: {lon}")

        # Validate coordinates
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            print("Invalid coordinates")
            return

        # Center the map on the coordinates
        self.map_widget.setCenter(lat, lon, 10)

        # Save the map as an HTML file
        html_file = os.path.abspath('map.html')
        self.map_widget.to_html(html_file)

        # Load the HTML file in the QWebEngineView
        self.web_view.setUrl(QUrl.fromLocalFile(html_file))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
