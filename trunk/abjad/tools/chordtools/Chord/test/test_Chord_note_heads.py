# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Chord_note_heads_01():
    r'''Chord returns note heads as an immutable tuple.
    '''

    chord = Chord("<d' e' f'>4")
    note_heads = chord.note_heads

    assert isinstance(note_heads, tuple)
    assert len(note_heads) == 3
    assert py.test.raises(Exception, 'note_heads.pop()')
    assert py.test.raises(Exception, 'note_heads.remove(note_heads[0])')


def test_Chord_note_heads_02():
    r'''Note heads of chords with equivalent pitches compare equal.
    '''

    chord_1 = Chord("<d' e' f'>4")
    chord_2 = Chord("<d' e' f'>4")

    assert chord_1.note_heads == chord_2.note_heads


def test_Chord_note_heads_03():
    r'''Note heads can be assigned with a LilyPond input string.
    '''

    chord = Chord("<c'>4")
    chord.note_heads = "c' d' e'"

    assert chord.lilypond_format == "<c' d' e'>4"


def test_Chord_note_heads_04():
    r'''Set note head color with the LilyPond tweak reservoir.
    '''

    chord = Chord("<ef' cs'' f''>4")
    chord[0].tweak.color = 'red'
    chord[1].tweak.color = 'green'
    chord[2].tweak.color = 'blue'

    r'''
    <
        \tweak #'color #red
        ef'
        \tweak #'color #green
        cs''
        \tweak #'color #blue
        f''
    >4
    '''

    assert chord.lilypond_format == "<\n\t\\tweak #'color #red\n\tef'\n\t\\tweak #'color #green\n\tcs''\n\t\\tweak #'color #blue\n\tf''\n>4"
