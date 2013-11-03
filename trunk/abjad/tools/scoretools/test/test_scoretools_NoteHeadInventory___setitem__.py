# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___setitem___01():
    r'''Set note head with pitch number.
    '''

    chord = Chord("<c' d'>4")
    chord[1] = 4

    assert chord.lilypond_format == "<c' e'>4"


def test_scoretools_Chord___setitem___02():
    '''Set note head with pitch.
    '''

    chord = Chord("<c' d'>4")
    chord[1] = pitchtools.NamedPitch("e'")

    assert chord.lilypond_format == "<c' e'>4"


def test_scoretools_Chord___setitem___03():
    r'''Set note head with tweaked note head.
    '''

    chord = Chord("<c' cs'' f''>4")
    note_head = scoretools.NoteHead(3)
    note_head.tweak.color = 'red'
    chord[0] = note_head

    assert testtools.compare(
        chord,
        r'''
        <
            \tweak #'color #red
            ef'
            cs''
            f''
        >4
        '''
        )

    assert inspect(chord).is_well_formed()
