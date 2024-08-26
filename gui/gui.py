import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI testing/learning")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
    
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

       
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        
        folium_map = folium.Map(
            location=[33.53210, -5.10950],
            zoom_start=13,
            tiles="CartoDB dark_matter", # dark theme
            min_zoom=3,
            max_bounds = True # Set the minimum zoom level
        )
         
        """cartodb positron"""
        folium.CircleMarker(location=[33.53210, -5.10950 ], fill=True).add_to(folium_map)

        
        html_file = os.path.abspath('folium_map.html')
        folium_map.save(html_file)

       
        self.web_view.setUrl(QUrl.fromLocalFile(html_file))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
