from abjad.tools.contexttools.Context import Context
from abjad.tools.lyricstools.Lyrics._LyricsFormatter import _LyricsFormatter


class Lyrics(Context):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None):
        Context.__init__(self, music)
        self.context_name = 'Lyrics'
        self._formatter = _LyricsFormatter(self)
