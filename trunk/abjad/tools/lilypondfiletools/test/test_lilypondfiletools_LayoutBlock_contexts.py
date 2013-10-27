# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondfiletools.LayoutBlock import LayoutBlock


def test_lilypondfiletools_LayoutBlock_contexts_01():
    r'''Layout block contexts list accepts line-literal iterables.
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

    assert testtools.compare(
        layout_block,
        r'''
        \layout {
            \context {
                \Voice
                \remove Forbid_line_break_engraver
            }
        }
        '''
        )
