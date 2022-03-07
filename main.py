import sys

# PyQt5 import
from PyQt5.QtWidgets import QApplication

# Media player GUI
from media import MediaPlayer


if __name__ == "__main__":

    # create an app instance
    app = QApplication(sys.argv)

    # create a new application window
    window = MediaPlayer()

    # exit window
    sys.exit(app.exec_())
