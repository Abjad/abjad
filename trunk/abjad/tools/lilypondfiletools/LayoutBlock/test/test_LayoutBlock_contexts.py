from abjad import *
from abjad.tools.lilypondfiletools.LayoutBlock import LayoutBlock


def test_LayoutBlock_contexts_01():
    '''Read-only layout block contexts list accepts line-literal iterables.
    '''

    layout_block = LayoutBlock()
    layout_block.contexts.append([r'\Voice', r'\remove Forbid_line_break_engraver'])

    r'''
    \layout {
        \context {
            \Voice
            \remove Forbid_line_break_engraver
        }
    }
    '''

    assert layout_block.format == '\\layout {\n\t\\context {\n\t\t\\Voice\n\t\t\\remove Forbid_line_break_engraver\n\t}\n}'
