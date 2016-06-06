# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Chord_note_heads_01():
    r'''Chord returns note heads as an immutable tuple.
    '''

    chord = Chord("<d' e' f'>4")
    note_heads = chord.note_heads

    assert isinstance(note_heads, scoretools.NoteHeadInventory)
    assert len(note_heads) == 3


def test_scoretools_Chord_note_heads_02():
    r'''Note heads of chords with equivalent pitches compare equal.
    '''

    chord_1 = Chord("<d' e' f'>4")
    chord_2 = Chord("<d' e' f'>4")

    assert chord_1.note_heads == chord_2.note_heads


def test_scoretools_Chord_note_heads_03():
    r'''Set note heads with pitch numbers.
    '''

    chord = Chord('<>4')
    chord.note_heads = [4, 3, 2]

    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord_note_heads_04():
    r'''Set note heads with pitches.
    '''

    chord = Chord('<>4')
    chord.note_heads = [
        NamedPitch(4),
        NamedPitch(3),
        NamedPitch(2),
        ]

    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord_note_heads_05():
    r'''Set note heads with both pitches and pitch numbers.
    '''

    chord = Chord('<>4')
    chord.note_heads = [
        NamedPitch(4),
        3,
        NamedPitch(2),
        ]

    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord_note_heads_06():
    r'''Set note heads with a LilyPond input string.
    '''

    chord = Chord("<c'>4")
    chord.note_heads = "c' d' e'"

    assert format(chord) == "<c' d' e'>4"


def test_scoretools_Chord_note_heads_07():
    r'''Set note head color with the LilyPond tweak reservoir.
    '''

    chord = Chord("<ef' cs'' f''>4")
    chord.note_heads[0].tweak.color = 'red'
    chord.note_heads[1].tweak.color = 'green'
    chord.note_heads[2].tweak.color = 'blue'

    assert format(chord) == stringtools.normalize(
        r'''
        <
            \tweak color #red
            ef'
            \tweak color #green
            cs''
            \tweak color #blue
            f''
        >4
        '''
        )
