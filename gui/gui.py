import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDockWidget, QWidget, QToolBar, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt


src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)


from ScoreCache import ScoreCache
from Processing.CoordinateGenerator import CoordinateGenerator
from Config.config import RADIUS, LAT, LON

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        self.score_cache = None
        self.score_cache = self._initialize_system(LAT, LON) 
        self._initializeUI()
        


    def _initializeUI(self):
        self._create_central_widget()
        self._create_toolbar()
        self._create_sidebar()
        self._create_web_view()
        
        if self.score_cache is not None:
            self._display_folium_map()
        else:
            print("Error initializing the system, score cache is None")
            exit(1)

    def _create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

    def _create_sidebar(self):
        sidebar = QDockWidget("Controls", self)
        sidebar.setAllowedAreas(Qt.LeftDockWidgetArea)
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)
        test_button = QPushButton("Test Button")
        sidebar_layout.addWidget(test_button)
        sidebar.setWidget(sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, sidebar)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        sidebar.setGraphicsEffect(opacity_effect)

    def _create_web_view(self):
        self.web_view = QWebEngineView()
        self.centralWidget().layout().addWidget(self.web_view)

    def _display_folium_map(self):
        map_location = [LAT, LON]
        zoom_start = 13
        tiles = "CartoDB dark_matter"

        # Create Folium map
        folium_map = folium.Map(
            location=map_location,
            zoom_start=zoom_start,
            tiles=tiles,
            min_zoom=3,
            max_bounds=True
        )

        html_file = os.path.abspath('folium_map.html')
        self._render_best_coordinates(folium_map)
        folium_map.save(html_file)
        self.web_view.setUrl(QUrl.fromLocalFile(html_file))

    def _initialize_system(self, lat, lon):
        coordinates_generator = CoordinateGenerator(10)
        coordinates = coordinates_generator.generate_grid_in_circle(lat, lon, RADIUS)
        score_cache = ScoreCache(coordinates)
        score_cache.calculate_and_add_scores_bulk(coordinates)
        return score_cache

    def _get_best_coordinates(self, score_cache):
        best_coordinates = score_cache._get_best_coordinates(10) # Get the top 10 coordinates
        return best_coordinates

    def _render_best_coordinates(self, map):
        best_coordinates = self._get_best_coordinates(self.score_cache)
        for coordinate, score in best_coordinates:
            popup_html = f"""
            <b>Coordinates:</b> {coordinate[0]:.6f}, {coordinate[1]:.6f}<br>
            <b>Score:</b> {score}<br>
            <b>Description:</b> This is a point of interest.
            """
            folium.Marker(
                location=coordinate,
                popup=folium.Popup(popup_html, max_width=300)  # You can set max_width for the popup
            ).add_to(map)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
