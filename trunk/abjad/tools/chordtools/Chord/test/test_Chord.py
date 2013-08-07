# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_Chord_01():

    chord = Chord([2, 3, 4], (1, 4))
    assert str(chord) == "<d' ef' e'>4"
    assert chord.lilypond_format == "<d' ef' e'>4"
    assert len(chord) == 3
    assert len(chord.note_heads) == 3
    assert len(chord.written_pitches) == 3
    assert chord.written_duration == chord.get_duration() == Duration(1, 4)


def test_Chord_02():
    r'''Chord with tweaked note head.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    chord[0].tweak.style = 'harmonic'
    assert testtools.compare(
        chord.lilypond_format,
        r'''
        <
            \tweak #'style #'harmonic
            d'
            ef'
            e'
        >4
        '''
        )


def test_Chord_03():
    chord = Chord([2, 3, 4], (1, 4))
    chord[0].tweak.transparent = True
    assert testtools.compare(
        chord.lilypond_format,
        r'''
        <
            \tweak #'transparent ##t
            d'
            ef'
            e'
        >4
        '''
        )


def test_Chord_04():
    r'''Format one-note chord as chord.
    '''

    chord = Chord([0.5], (1, 4))
    assert str(chord) == "<cqs'>4"
    assert chord.lilypond_format == "<cqs'>4"
    assert len(chord) == 1
    assert len(chord.note_heads) == 1
    assert len(chord.written_pitches) == 1


def test_Chord_05():
    r'''Format chord with LilyPond command mark on right.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    marktools.LilyPondCommandMark('glissando', 'right')(chord)

    '''
    <d' ef' e'>4 \glissando
    '''

    assert chord.lilypond_format == "<d' ef' e'>4 \\glissando"


def test_Chord_06():
    r'''Format tweaked chord with LilyPond command mark on right.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    chord[0].tweak.color = 'red'
    marktools.LilyPondCommandMark('glissando', 'right')(chord)

    r'''
    <
        \tweak #'color #red
        d'
        ef'
        e'
    >4 \glissando
    '''

    assert testtools.compare(
        chord.lilypond_format,
        r'''
        <
            \tweak #'color #red
            d'
            ef'
            e'
        >4 \glissando
        '''
        )


def test_Chord_07():
    r'''Set chord pitches to numbers.
    '''

    chord = Chord([], (1,4))
    chord.written_pitches = [4, 3, 2]

    assert chord.lilypond_format == "<d' ef' e'>4"

    chord.written_pitches = (4, 3, 2)

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_08():
    r'''Set chord pitches to pitches.
    '''

    chord = Chord([], (1,4))
    chord.written_pitches = [pitchtools.NamedChromaticPitch(4), pitchtools.NamedChromaticPitch(3),
        pitchtools.NamedChromaticPitch(2)]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_09():
    r'''Set chord pitches to mixed numbers and pitches.
    '''

    chord = Chord([], (1,4))
    chord.written_pitches = [4, pitchtools.NamedChromaticPitch(3), pitchtools.NamedChromaticPitch(2)]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_10():
    r'''Set chord note heads to numbers.
    '''

    chord = Chord([], (1,4))
    chord.note_heads = [4, 3, 2]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_11():
    r'''Set chord note heads to pitches.
    '''

    chord = Chord([], (1,4))
    chord.note_heads = [pitchtools.NamedChromaticPitch(4), pitchtools.NamedChromaticPitch(3), pitchtools.NamedChromaticPitch(2)]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_12():
    r'''Set chord note heads to mixed numbers and pitches.
    '''

    chord = Chord([], (1,4))
    chord.note_heads = [pitchtools.NamedChromaticPitch(4), 3, pitchtools.NamedChromaticPitch(2)]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_13():
    r'''Set chord item to pitch or number.
    '''

    t = Chord([2, 4], (1,4))
    t[0] = pitchtools.NamedChromaticPitch(5)
    assert t.lilypond_format == "<e' f'>4"

    t[0] = 7
    assert t.lilypond_format == "<f' g'>4"
