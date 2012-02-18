from abjad.tools.contexttools._Context import _Context
from abjad.tools.lyricstools.Lyrics._LyricsFormatter import _LyricsFormatter


class Lyrics(_Context):

    def __init__(self, music=[]):
        _Context.__init__(self, music)
        self.context = 'Lyrics'
        self._formatter = _LyricsFormatter(self)
