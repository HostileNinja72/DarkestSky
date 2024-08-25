import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import geemap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Earth Engine with PyQt5")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.map_widget = geemap.Map()
        self.setCentralWidget(self.map_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
