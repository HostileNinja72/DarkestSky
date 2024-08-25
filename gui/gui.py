
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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        #QWebEngineView
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        #geemap
        self.map_widget = geemap.Map()
        self.map_widget.add_basemap('HYBRID')

        
        html_file = os.path.abspath('map.html')
        self.map_widget.to_html(html_file)

        self.web_view.setUrl(QUrl.fromLocalFile(html_file))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
