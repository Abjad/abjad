# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class LayoutBlock(AttributedBlock):
    r'''Abjad model of LilyPond input file layout block:

    ::

        >>> layout_block = lilypondfiletools.LayoutBlock()

    ::

        >>> layout_block
        LayoutBlock()

    ::

        >>> layout_block.indent = 0
        >>> layout_block.ragged_right = True

    ..  doctest::

        >>> f(layout_block)
        \layout {
            indent = #0
            ragged-right = ##t
        }

    Returns layout block.
    '''

    ### INITIALIZER ###

    def __init__(self):
        AttributedBlock.__init__(self)
        self._escaped_name = r'\layout'
        self._context_blocks = []
        self._contexts = []

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_context_blocks(self):
        result = []
        for context_block in self.context_blocks:
            result.extend(context_block._format_pieces)
        return result

    @property
    def _formatted_context_specifications(self):
        result = []
        for context_specification in self.contexts:
            result.append(r'\context {')
            for x in context_specification:
                result.append('\t' + str(x))
            result.append('}')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def context_blocks(self):
        r'''List of context blocks:

        ::

            >>> layout_block = lilypondfiletools.LayoutBlock()

        ::

            >>> context_block = lilypondfiletools.ContextBlock('Score')
            >>> override(context_block).bar_number.transparent = True

        ::

            >>> scheme_expr = schemetools.Scheme('end-of-line-invisible')
            >>> override(context_block).time_signature.break_visibility = \
            ...     scheme_expr
            >>> layout_block.context_blocks.append(context_block)

        ..  doctest::

            >>> f(layout_block)
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

    @property
    def contexts(self):
        r'''DEPRECATED. USE CONTEXT_BLOCKS INSTEAD.
        '''
        return self._contexts
