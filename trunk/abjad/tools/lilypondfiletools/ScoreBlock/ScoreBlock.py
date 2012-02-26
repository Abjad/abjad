from abjad.tools.lilypondfiletools._NonattributedBlock import _NonattributedBlock


class ScoreBlock(_NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file score block::

        abjad> score_block = lilypondfiletools.ScoreBlock()

    ::

        abjad> score_block
        ScoreBlock()

    ::

        abjad> score_block.append(Staff([]))
        abjad> f(score_block)
        \score {
            \new Staff {
            }
        }

    ScoreBlocks does not format when empty, as this generates a 
    parser error in LilyPond::

        abjad> score_block = lilypondfiletools.ScoreBlock()
        abjad> score_block.format == ''
        True

    Return score block.
    '''

    def __init__(self):
        _NonattributedBlock.__init__(self)
        self._escaped_name = r'\score'
        self._is_formatted_when_empty = False
