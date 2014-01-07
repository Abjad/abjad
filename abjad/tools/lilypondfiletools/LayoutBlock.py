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
        self._context_blocks = []

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_context_blocks(self):
        result = []
        for context_block in self.context_blocks:
            result.extend(context_block._format_pieces)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def context_blocks(self):
        r'''Gets context blocks in ``\layout`` block.

        ..  container:: example

            ::

                >>> block = lilypondfiletools.ContextBlock(
                ...     source_context_name='Score',
                ...     )
                >>> override(block).bar_number.transparent = True
                >>> scheme = schemetools.Scheme('end-of-line-invisible')
                >>> override(block).time_signature.break_visibility = scheme
                >>> layout_block = lilypondfiletools.LayoutBlock()
                >>> layout_block.context_blocks.append(block)

            ::

                >>> print format(layout_block)
                \layout {
                    \context {
                        \Score
                        \override BarNumber #'transparent = ##t
                        \override TimeSignature #'break-visibility = #end-of-line-invisible
                    }
                }

        Returns list.
        '''
        return self._context_blocks
