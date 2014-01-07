# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import override
from abjad.tools.lilypondfiletools.Block import Block


class LayoutBlock(Block):
    r'''A LilyPond file ``\layout`` block.

    ..  container:: example

        ::

            >>> layout_block = lilypondfiletools.LayoutBlock()
            >>> layout_block.indent = 0
            >>> layout_block.ragged_right = True

        ::

            >>> print format(layout_block)
            \layout {
                indent = #0
                ragged-right = ##t
            }

    '''

    ### INITIALIZER ###

    def __init__(self):
        Block.__init__(self, name='layout')

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_context_blocks(self):
        from abjad.tools import lilypondfiletools
        result = []
        context_blocks = []
        for item in self.items:
            if isinstance(item, lilypondfiletools.ContextBlock):
                context_blocks.append(item)
        for context_block in context_blocks:
            result.extend(context_block._format_pieces)
        return result
