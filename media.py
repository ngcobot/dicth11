import os

from player import Player
from view.ui import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon


class MediaPlayer(QMainWindow, Ui_MainWindow):
    """
    Media player (GUI)
    """

    def __init__(self, *args, **kwargs):
        super(MediaPlayer, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Player Instance
        self.player = Player()

        # Initilise UI
        self.initialise_ui()

        self.show()

    def initialise_ui(self):
        """
        Initialise MainWindow UI
        """
        # Default sceen size
        self.width = 720
        self.height = 480

        # Get the desktop screen geometry
        self._SCREEN_WIDTH = QApplication.desktop().width()
        self._SCREEN_HEIGHT = QApplication.desktop().height()

        # center MainWindow on screen
        self.y_pos = int((self._SCREEN_WIDTH - self.width) / 2)
        self.x_pos = int((self._SCREEN_HEIGHT - self.height) / 2)

        self.setGeometry(self.y_pos, self.x_pos, self.width, self.height)

        # MainWindow Title
        self.window_title = "Everest Media"
        self.setWindowTitle(self.window_title)

        # Application icon
        self.setWindowIcon(QIcon(os.path.join("src", "icons", "icon.png")))

        # Bind vlc Instance to Qt Widget
        self.player.set_window(self.videoFrame.winId())

        # Hide playlist widget
        self.mainFrame.hide()
