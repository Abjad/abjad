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

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import leaftools
        result = []
        if not len(self):
            if self._is_formatted_when_empty:
                result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            if len(self) == 1 and isinstance(self[0], leaftools.Leaf):
                result.append('\t{')
                result.extend(['\t\t' + piece for piece in self[0]._format_pieces])
                result.append('\t}')
            else:
                for x in self:
                    if hasattr(x, '_get_format_pieces'):
                        result.extend(['\t' + piece for piece in x._get_format_pieces()])
                    elif hasattr(x, '_format_pieces'):
                        result.extend(['\t' + piece for piece in x._format_pieces])
                    elif isinstance(x, str):
                        result.append('\t%s' % x)
            result.append('}')
        return result

