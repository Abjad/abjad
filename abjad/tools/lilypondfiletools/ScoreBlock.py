# -*- encoding: utf-8 -*-
#from abjad.tools.lilypondfiletools.NonattributedBlock \
#    import NonattributedBlock
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


#class ScoreBlock(NonattributedBlock):
class ScoreBlock(AttributedBlock):
    r'''Abjad model of LilyPond input file score block:

    ::

        >>> score_block = lilypondfiletools.ScoreBlock()

    ::

        >>> score_block
        ScoreBlock()

    ::

        >>> score_block.items.append(Staff([]))
        >>> print format(score_block)
        \score {
            \new Staff {
            }
        }

    '''

    ### INITIALIZER ###

    def __init__(self):
        #NonattributedBlock.__init__(self)
        AttributedBlock.__init__(self)
        self._escaped_name = r'\score'

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        result = []
        if not len(self.items):
            result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            if len(self.items) == 1 and \
                isinstance(self.items[0], (scoretools.Leaf, markuptools.Markup)):
                result.append('\t{')
                result.extend(
                    ['\t\t' + piece for piece in self.items[0]._format_pieces])
                result.append('\t}')
            else:
                for x in self.items:
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
