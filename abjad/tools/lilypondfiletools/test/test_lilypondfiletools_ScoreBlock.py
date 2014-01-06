# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_ScoreBlock_01():
    r'''MIDI block is formatted when empty by default.
    Layout block must be explicitly set to format when empty.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score_block = lilypondfiletools.ScoreBlock()
    layout_block = lilypondfiletools.LayoutBlock()
    midi_block = lilypondfiletools.Block(name='midi')

    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    assert systemtools.TestManager.compare(
        score_block,
        r'''
        \score {
            \new Score <<
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
            \layout {}
            \midi {}
        }
        '''
        )
