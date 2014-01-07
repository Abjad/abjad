# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class ScoreBlock(Block):
    r'''A LilyPond file ``\score`` block.

    ..  container:: example

        ::

            >>> score_block = lilypondfiletools.ScoreBlock()
            >>> score_block.items.append(Score([]))

        ::

            >>> print format(score_block)
            \score {
                \new Score <<
                >>
            }

    '''

    ### INITIALIZER ###

    def __init__(self):
        Block.__init__(self, name='score')

    ### PRIVATE PROPERTIES ###

#    @property
#    def _format_pieces(self):
#        result = []
#        if not len(self.items):
#            string = r'{} {{}}'.format(self._escaped_name)
#            result.append(string)
#        else:
#            string = r'{} {{'.format(self._escaped_name)
#            result.append(string)
#            prototype = (scoretools.Leaf, markuptools.Markup)
#            if len(self.items) == 1 and isinstance(self.items[0], prototype):
#                result.append('\t{')
#                pieces = self.items[0]._format_pieces
#                pieces = ['\t\t' + item for item in pieces]
#                result.extend(pieces)
#                result.append('\t}')
#            else:
#                for item in self.items:
#                    if isinstance(item, str):
#                        string = '\t{}'.format(item)
#                        result.append(string)
#                    elif hasattr(item, '_get_format_pieces'):
#                        pieces = item._get_format_pieces()
#                        pieces = ['\t' + item for item in pieces]
#                        result.extend(pieces)
#                    else:
#                        pieces = item._format_pieces
#                        pieces = ['\t' + item for item in pieces]
#                        result.extend(pieces)
#            result.append('}')
#        return result
