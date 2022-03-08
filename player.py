import sys
import vlc


class Player:
    """
    VLC wrapper class
    """

    def __init__(self):
        """
        Init class
        Creates a media list player and playlist
        """

        # Create media player
        self.media = vlc.MediaListPlayer()

        # Create a media instace of the player
        self.m_instance = self.media.get_media_player()

        # Media playlist
        self.playlist = vlc.MediaList()

        # Set default media plsylist mode loop through all the media
        self.media.set_playback_mode(vlc.PlaybackMode.loop)

        # Set media playlist
        self.media.set_media_list(self.playlist)

    def add_media(self, mrls):
        """
        Add media to playlist
        """
        # for file in mrls:
        #     self.playlist.add_media(file)
        [self.playlist.add_media(file) for file in mrls]

    def play(self):
        """
        Play media playlist
        """
        self.media.play()

    def stop(self):
        """
        Stop playing media list.
        """
        return self.media.stop()

    def pause(self):
        """
        Toggle pause (or resume) media list.
        """
        self.media.pause()

    def resume(self):
        """
        Pause or resume media list.
        """
        self.media.set_pause(0)

    def next(self):
        """
        Play next item from media list.
        @return: 0 upon success -1 if there is no next item.
        """
        return self.media.next()

    def previous(self):
        """
        Play previous item from media list.
        @return: 0 upon success -1 if there is no previous item.
        """
        # self.media.get_media_player().get_media().release()
        return self.media.previous()

    def stop(self):
        """
        Stop playing media list.
        """
        return self.media.stop()

    def mute_audio(self):
        """
        Mute media audio
        """
        m_status = self.m_instance.audio_get_mute()
        if not m_status:
            self.m_instance.audio_set_mute(True)
        else:
            self.m_instance.audio_set_mute(False)

    def volume_up(self):
        """
        Set current software audio volume.
        """
        current_volume = self.m_instance.audio_get_volume()
        if current_volume <= 190:
            return self.m_instance.audio_set_volume(current_volume + 5)

    def volume_down(self):
        """
        Set current software audio volume.
        """
        current_volume = self.m_instance.audio_get_volume()
        if current_volume >= 0:
            return self.m_instance.audio_set_volume(current_volume - 5)

    def is_playing(self):
        """
        Is media list playing?
        @return: true for playing and false for not playing
        """
        return self.media.is_playing()

    def get_state(self):
        """
        Get current state of media list player.
        @return: State for media list player from vlc.State
        """
        return self.media.get_state()

    def playlist_count(self):
        """
        Playist count
        """
        return self.playlist.count()

    def get_title(self):
        """
        Get movie title.
        @return: title number currently playing, or -1.
        """
        media = self.m_instance.get_media()

        if media is None:
            return ""

        media.parse_with_options(
            vlc.MediaParseFlag.local, -1
        )  # parse the current media

        title = f"{media.get_meta(0)}" or ""

        # stop aprsing the media
        media.parse_stop()

        return title

    def get_media_length(self):
        """
        Get paying media length in ms
        """
        return self.convert_ms(self.media.get_media_player().get_length())

    def next_frame(self):
        """
        Get the nest frame on the media
        """
        return self.m_instance.next_frame()

    def set_time(self, time_ms):
        """
        Set the movie time (in ms).
        @param time_ms: the movie time (in ms).
        """
        self.m_instance.set_time(time_ms)

    def get_media_current_time(self):
        """
        Media current time
        """
        return self.m_instance.get_time()

    def fast_forward(self):
        """
        10 seconds fast forward
        """
        duration = self.media.get_media_player().get_length()
        time = int(self.get_media_current_time())

        # check if the media is 1s from ending
        if (time + 130) > duration:
            return
        # play the next media if media has reached end of duration
        elif (time + 120) >= duration:
            # self.player.set_time(duration)
            self.next()

        else:
            self.set_time(time + 10000)

    def back_forward(self):
        """
        Backward skip media time by 10s
        """
        time = int(self.get_media_current_time())  # media running time

        if time - 10000 < 0:
            self.set_time(0)
        else:
            self.set_time(abs(time - 10000))

    def set_window(self, wm_id):
        """
        Set an X Window System drawable where the media player should render its video output.
        """
        # the media player has to be 'connected' to the QWidget
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.m_instance.set_xwindow(wm_id)
        elif sys.platform == "win32":  # for Windows
            self.m_instance.set_hwnd(wm_id)
        elif sys.platform == "darwin":  # for MacOS
            self.m_instance.set_nsobject(wm_id)

    @staticmethod
    # Convert millis to format  hr:min:ss format
    def convert_ms(millis: int):
        """
        Convert duration(ms) to hr:min:ss format
        """
        if millis < 0:
            return f"{int(0):02d}:{int(0):02d}"

        seconds, millis = divmod(millis, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours:
            return f"{hours}:{int(minutes):02d}:{int(seconds):02d}"  # hr:min:ss
        else:
            return f"{int(minutes):02d}:{int(seconds):02d}"  # min:ss
