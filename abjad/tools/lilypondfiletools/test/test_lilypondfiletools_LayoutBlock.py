# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LayoutBlock_01():

    lb = lilypondfiletools.LayoutBlock()
    lb.indent = 0
    lb.ragged_right = True

    r'''
    \layout {
        indent = #0
        ragged-right = ##t
    }
    '''

    assert systemtools.TestManager.compare(
        lb,
        r'''
        \layout {
            indent = #0
            ragged-right = ##t
        }
        '''
        )


def test_lilypondfiletools_LayoutBlock_02():

    lb = lilypondfiletools.LayoutBlock()
    m = indicatortools.LilyPondCommand('accidentalStyle modern')
    lb.append(m)

    r'''
    \layout {
        \accidentalStyle modern
    }
    '''

    assert systemtools.TestManager.compare(
        lb,
        r'''
        \layout {
            \accidentalStyle modern
        }
        '''
        )
