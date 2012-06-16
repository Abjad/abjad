from abjad.tools.lilypondfiletools.NonattributedBlock import NonattributedBlock


class ScoreBlock(NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file score block::

        >>> score_block = lilypondfiletools.ScoreBlock()

    ::

        >>> score_block
        ScoreBlock()

    ::

        >>> score_block.append(Staff([]))
        >>> f(score_block)
        \score {
            \new Staff {
            }
        }

    ScoreBlocks does not format when empty, as this generates a 
    parser error in LilyPond::

        >>> score_block = lilypondfiletools.ScoreBlock()
        >>> score_block.lilypond_format == ''
        True

    Return score block.
    '''

    def __init__(self):
        NonattributedBlock.__init__(self)
        self._escaped_name = r'\score'
        self._is_formatted_when_empty = False
