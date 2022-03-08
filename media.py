import os
from pathlib import Path


from player import Player
from view.ui import Ui_MainWindow
from modules.helper import scan_files

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMenu, QFileDialog
from PyQt5.QtGui import QIcon


class MediaPlayer(QMainWindow, Ui_MainWindow):
    """
    Media player (GUI)
    """

    # defaults
    home_directory = os.environ.get("HOME")
    default_dir = os.path.join(home_directory, "Videos")

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
            self.update()
        elif action == open_file:
            self.open_files()
        elif action == open_dir:
            self.open_folder()
        elif action == next_button:
            self.player.next()
            print(self.player.get_title())
        elif action == previous_button:
            self.player.previous()
        elif action == playlist_button:
            # TODO : Add playlist video mode toggle
            self.player.pause()

    def open_files(self):
        """
        Open media files
        """

        file, _ = QFileDialog.getOpenFileNames(
            self,
            "Open file",
            MediaPlayer.default_dir,
            "MPEG-4 (*.bin *.mp4);;"
            "All files (*.mp4* *.mp3* *.bin* *.mkv* *.avi* *.webm*)",
        )

        self.set_uri(file)

    def open_folder(self):
        """
        Open a folder and look for media files to play
        """

        files_found = QFileDialog.getExistingDirectory(
            self,
            "Open Dir",
            self.default_dir,
            QFileDialog.DontResolveSymlinks,
        )

        _, files = scan_files(files_found, ".mp4")

        files.sort(key=os.path.getctime)

        self.set_uri(files)

    def dragEnterEvent(self, event):
        """
        Listen to drag enter events i.e accept drag enter events
        """
        event.accept()

    def dropEvent(self, event) -> None:
        """
        Drop media onto application to play -  event handler

        """
        # scan through the url/folders draged
        #  to the mainwindow to play media
        files = self.convert_qurl_path(event.mimeData().urls())
        self.set_uri(files)

    def set_uri(self, mrls):
        """
        Set media uri an play items
        """
        self.player.add_media(mrls)
        if not self.player.is_playing():
            self.player.play()

    @staticmethod
    def convert_qurl_path(urls):
        """
        Convert QUrl to Path(linux)
        """
        url_path = []
        _found_files = []

        # clean urls to paths
        for url in urls:
            # Convert QUrl to Path(linux)
            url_path.append(Path(url.path()))

            # check for folders and files
        for path in url_path:
            # Get the files matching the extension from the folder
            if path.is_dir():
                _, files = scan_files(path, ".mp4")
                [_found_files.append(file) for file in files]
            elif path.is_file():
                # files.append(os.fspath(path))
                _found_files.append(os.fspath(path))

        return _found_files

    def mouseDoubleClickEvent(self, *event):
        """
        Listen to mouse double click event and toggle UI fullscreen
        """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
