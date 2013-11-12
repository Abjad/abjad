# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.NonattributedBlock \
    import NonattributedBlock


class ScoreBlock(NonattributedBlock):
    r'''Abjad model of LilyPond input file score block:

    ::

        >>> score_block = lilypondfiletools.ScoreBlock()

    ::

        >>> score_block
        ScoreBlock()

    ::

        >>> score_block.append(Staff([]))
        >>> print format(score_block)
        \score {
            \new Staff {
            }
        }

    ScoreBlocks does not format when empty, as this generates a
    parser error in LilyPond:

    ::

        >>> score_block = lilypondfiletools.ScoreBlock()
        >>> format(score_block) == ''
        True

    Returns score block.
    '''

    ### INITIALIZER ###

    def __init__(self):
        NonattributedBlock.__init__(self)
        self._escaped_name = r'\score'
        self._is_formatted_when_empty = False

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        result = []
        if not len(self):
            if self._is_formatted_when_empty:
                result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            if len(self) == 1 and \
                isinstance(self[0], (scoretools.Leaf, markuptools.Markup)):
                result.append('\t{')
                result.extend(
                    ['\t\t' + piece for piece in self[0]._format_pieces])
                result.append('\t}')
            else:
                for x in self:
                    if isinstance(x, str):
                        result.append('\t%s' % x)
                    elif hasattr(x, '_get_format_pieces'):
                        result.extend(
                            ['\t' + piece for piece in x._get_format_pieces()])
                    else:
                        result.extend(
                            ['\t' + piece for piece in x._format_pieces])
            result.append('}')
        return result
