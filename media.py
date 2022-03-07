from view.ui import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow


class MediaPlayer(QMainWindow, Ui_MainWindow):
    """
    Media player (GUI)
    """

    def __init__(self, *args, **kwargs):
        super(MediaPlayer, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.show()
