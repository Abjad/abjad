from abjad.tools.contexttools.Context import Context
from abjad.tools.lyricstools.Lyrics._LyricsFormatter import _LyricsFormatter


class Lyrics(Context):

    def __init__(self, music=[]):
        Context.__init__(self, music)
        self.context = 'Lyrics'
        self._formatter = _LyricsFormatter(self)
