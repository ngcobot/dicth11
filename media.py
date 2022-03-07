import os

from player import Player
from view.ui import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMenu
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

    def contextMenuEvent(self, event):
        """
        Context menu
        """
        context_menu = QMenu(self)

        if self.player.is_playing():
            button_text = "Pause"
        else:
            button_text = "Play"

        play_button = context_menu.addAction(button_text)
        stop_button = context_menu.addAction("Stop")
        next_button = context_menu.addAction("Next")
        previous_button = context_menu.addAction("Previous")

        context_menu.addSeparator()
        playlist_button = context_menu.addAction("Playlist")

        impMenu = QMenu("Open Media", self)
        open_file = QAction("Open File..", self)
        open_dir = QAction("Open Directory..", self)
        impMenu.addAction(open_file)
        impMenu.addAction(open_dir)
        sub_menu = context_menu.addMenu(impMenu)

        context_menu.addSeparator()
        quitAct = context_menu.addAction("Quit")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()
        elif action == play_button:
            self.player.pause()
        elif action == stop_button:
            self.player.stop()
            self.reset_ui()
        elif action == open_file:
            self.open_files()
        elif action == open_dir:
            self.open_folder()
        elif action == next_button:
            self.player.next()
            print(self.player.get_title())
        elif action == previous_button:
            self.player.previous_media()
            print(self.player.get_title())
        elif action == playlist_button:
            # self.videoFrame.hide()
            self.player.pause()
            self.frame_2.show()
            self.treeWidget.show()
            self.update()
