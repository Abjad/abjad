from abjad.tools.lilypondfiletools._NonattributedBlock import _NonattributedBlock


class ScoreBlock(_NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file score block.
    '''

    def __init__(self):
        _NonattributedBlock.__init__(self)
        self._escaped_name = r'\score'
