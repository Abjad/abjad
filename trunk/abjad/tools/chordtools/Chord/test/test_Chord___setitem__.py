# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord___setitem___01():
    r'''Set item with pitch number.
    '''

    chord = Chord("<c' d'>4")
    chord[1] = 4

    assert chord.lilypond_format == "<c' e'>4"


def test_Chord___setitem___02():
    '''Set item with pitch.
    '''

    chord = Chord("<c' d'>4")
    chord[1] = pitchtools.NamedChromaticPitch("e'")

    assert chord.lilypond_format == "<c' e'>4"


def test_Chord___setitem___03():
    r'''Set item with tweaked note head.
    '''

    chord = Chord("<c' cs'' f''>4")
    note_head = notetools.NoteHead(3)
    note_head.tweak.color = 'red'
    chord[0] = note_head

    assert testtools.compare(
        chord.lilypond_format,
        r'''
        <
            \tweak #'color #red
            ef'
            cs''
            f''
        >4
        '''
        )
