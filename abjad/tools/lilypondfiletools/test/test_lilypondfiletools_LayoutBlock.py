# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LayoutBlock_01():

    layout_block = lilypondfiletools.LayoutBlock()
    layout_block.indent = 0
    layout_block.ragged_right = True

    assert systemtools.TestManager.compare(
        layout_block,
        r'''
        \layout {
            indent = #0
            ragged-right = ##t
        }
        '''
        )


def test_lilypondfiletools_LayoutBlock_02():

    layout_block = lilypondfiletools.LayoutBlock()
    command = indicatortools.LilyPondCommand('accidentalStyle modern')
    layout_block.items.append(command)

    assert systemtools.TestManager.compare(
        layout_block,
        r'''
        \layout {
            \accidentalStyle modern
        }
        '''
        )
