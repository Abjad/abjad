from abjad.tools.contexttools.Context._ContextFormatter import _ContextFormatter


class _LyricsFormatter(_ContextFormatter):

    def __init__(self, client):
        _ContextFormatter.__init__(self, client)
