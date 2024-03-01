
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, pyqtSignal

from bot import Bot
class MainWindow(QMainWindow):

    
    increase_loading_bar = pyqtSignal()
    decrease_loading_bar = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.bot=Bot(window=None)
        #connect ths signal by the two functions of the increase and decrease
        self.increase_loading_bar.connect(self.increase_loading)
        self.decrease_loading_bar.connect(self.decrease_loading)

        self.setWindowTitle("Loading Bar")

        self.loading_bar = QProgressBar(self)
        self.loading_bar.setGeometry(30, 30, 25, 340)  # Adjusting position and size
        self.loading_bar.setOrientation(Qt.Orientation.Vertical)  # Setting orientation to vertical

        self.loading_value = 0
        self.loading_bar.setValue(self.loading_value)

        self.percentage_label = QLabel(self)
        self.percentage_label.setGeometry(65, 30, 50, 25)  # Adjusting position and size
        self.update_percentage_label()

        # Fit window size to the size of the bar and label
        window_width = self.loading_bar.width() + self.loading_bar.x() + 100  # Adding extra space
        window_height = self.loading_bar.height() + self.loading_bar.y() + 50  # Adding extra space

        screen_geometry = QApplication.primaryScreen().geometry()
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

    def update_percentage_label(self):
        self.percentage_label.setText(f"{self.loading_value}%")

    def increase_loading(self):
        self.loading_value = min(100, self.loading_value + 2)
        self.loading_bar.setValue(self.loading_value)
        self.update_percentage_label()

    def decrease_loading(self):
        self.loading_value = max(0, self.loading_value - 2)
        self.loading_bar.setValue(self.loading_value)
        self.update_percentage_label()         

    def equalBots(self,bot):
        self.bot=bot

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        print("here")
        self.bot.closee()
        return super().closeEvent(a0)        