from abjad.tools.lilypondfiletools._NonattributedBlock import _NonattributedBlock


class ScoreBlock(_NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file score block::

        abjad> score_block = lilypondfiletools.ScoreBlock()

    ::

        abjad> score_block
        ScoreBlock()

    ::

        abjad> f(score_block)
        \score {}

    Return score block.
    '''

    def __init__(self):
        _NonattributedBlock.__init__(self)
        self._escaped_name = r'\score'
