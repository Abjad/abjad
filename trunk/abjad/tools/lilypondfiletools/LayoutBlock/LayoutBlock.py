from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class LayoutBlock(AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file layout block::

        >>> layout_block = lilypondfiletools.LayoutBlock()

    ::

        >>> layout_block
        LayoutBlock()

    ::

        >>> layout_block.indent = 0
        >>> layout_block.ragged_right = True

    ::

        >>> f(layout_block)
        \layout {
            indent = #0
            ragged-right = ##t
        }

    Return layout block.
    '''

    def __init__(self):
        AttributedBlock.__init__(self)
        self._escaped_name = r'\layout'
        self._context_blocks = []
        self._contexts = []

    # PRIVATE ATTRIUBTES #

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
        r'''Read-only list of context blocks::

            >>> layout_block = lilypondfiletools.LayoutBlock()

        ::

            >>> context_block = lilypondfiletools.ContextBlock('Score')
            >>> context_block.override.bar_number.transparent = True

        ::

            >>> scheme_expr = schemetools.Scheme('end-of-line-invisible')
            >>> context_block.override.time_signature.break_visibility = scheme_expr
            >>> layout_block.context_blocks.append(context_block)
    
        ::

            >>> f(layout_block)
            \layout {
                \context {
                    \Score
                    \override BarNumber #'transparent = ##t
                    \override TimeSignature #'break-visibility = #end-of-line-invisible
                }
            }

        Return list.
        '''
        return self._context_blocks

    @property
    def contexts(self):
        r'''DEPRECATED. USE CONTEXT_BLOCKS INSTEAD.'''
        return self._contexts
