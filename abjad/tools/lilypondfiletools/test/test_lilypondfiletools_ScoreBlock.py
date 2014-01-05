# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_ScoreBlock_01():
    r'''Midi block is formatted when empty by default.
    Layout block must be explicitly set to format when empty.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score_block = lilypondfiletools.ScoreBlock()
    layout_block = lilypondfiletools.LayoutBlock()
    layout_block.is_formatted_when_empty = True
    midi_block = lilypondfiletools.MIDIBlock()

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


def test_lilypondfiletools_ScoreBlock_02():
    r'''ScoreBlock does not format when empty by default.
    '''

    score_block = lilypondfiletools.ScoreBlock()
    assert format(score_block) == ''
