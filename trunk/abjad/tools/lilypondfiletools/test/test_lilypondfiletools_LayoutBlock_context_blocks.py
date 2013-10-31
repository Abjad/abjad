# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LayoutBlock_context_blocks_01():

    layout_block = lilypondfiletools.LayoutBlock()
    context_block = lilypondfiletools.ContextBlock('Score')
    override(context_block).bar_number.transparent = True
    override(context_block).time_signature.break_visibility = \
        schemetools.Scheme('end-of-line-invisible')
    layout_block.context_blocks.append(context_block)

    assert testtools.compare(
        layout_block,
        r'''
        \layout {
            \context {
                \Score
                \override BarNumber #'transparent = ##t
                \override TimeSignature #'break-visibility = #end-of-line-invisible
            }
        }
        '''
        )
