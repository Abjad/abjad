from abjad.tools.lilypondfiletools._BlockNonattributed import _BlockNonattributed


class ScoreBlock(_BlockNonattributed):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file score block.
    '''

    def __init__(self):
        _BlockNonattributed.__init__(self)
        self._escaped_name = r'\score'
