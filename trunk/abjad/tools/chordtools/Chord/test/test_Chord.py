from abjad import *
from py.test import raises


def test_Chord_01():
    t = Chord([2, 3, 4], (1, 4))
    assert str(t) == "<d' ef' e'>4"
    assert t.format == "<d' ef' e'>4"
    assert len(t) == 3
    assert len(t.note_heads) == 3
    assert len(t.written_pitches) == 3
    assert t.written_duration == t.prolated_duration == Duration(1, 4)


def test_Chord_02():
    '''Chord with tweaked note head.
    '''

    t = Chord([2, 3, 4], (1, 4))
    t[0].tweak.style = 'harmonic'
    assert t.format == "<\n\t\\tweak #'style #'harmonic\n\td'\n\tef'\n\te'\n>4"

def test_Chord_03():
    t = Chord([2, 3, 4], (1, 4))
    t[0].tweak.transparent = True
    assert t.format == "<\n\t\\tweak #'transparent ##t\n\td'\n\tef'\n\te'\n>4"


def test_Chord_04():
    '''Format one-note chord as chord.
    '''

    t = Chord([0.5], (1, 4))
    assert str(t) == "<cqs'>4"
    assert t.format == "<cqs'>4"
    assert len(t) == 1
    assert len(t.note_heads) == 1
    assert len(t.written_pitches) == 1


def test_Chord_05():
    '''Format chord with LilyPond command mark on right.
    '''

    chord = Chord([2, 3, 4], (1, 4))
    marktools.LilyPondCommandMark('glissando', 'right')(chord)

    '''
    <d' ef' e'>4 \glissando
    '''

    assert chord.format == "<d' ef' e'>4 \\glissando"


def test_Chord_06():
    '''Format tweaked chord with LilyPond command mark on right.
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

    assert chord.format == "<\n\t\\tweak #'color #red\n\td'\n\tef'\n\te'\n>4 \\glissando"


def test_Chord_07():
    '''Set chord pitches to numbers.
    '''

    t = Chord([], (1,4))
    t.written_pitches = [4, 3, 2]

    assert t.format == "<d' ef' e'>4"

    t.written_pitches = (4, 3, 2)

    assert t.format == "<d' ef' e'>4"


def test_Chord_08():
    '''Set chord pitches to pitches.
    '''

    t = Chord([], (1,4))
    t.written_pitches = [pitchtools.NamedChromaticPitch(4), pitchtools.NamedChromaticPitch(3), 
        pitchtools.NamedChromaticPitch(2)]

    assert t.format == "<d' ef' e'>4"


def test_Chord_09():
    '''Set chord pitches to mixed numbers and pitches.
    '''

    t = Chord([], (1,4))
    t.written_pitches = [4, pitchtools.NamedChromaticPitch(3), pitchtools.NamedChromaticPitch(2)]

    assert t.format == "<d' ef' e'>4"


def test_Chord_10():
    '''Set chord note heads to numbers.
    '''

    t = Chord([], (1,4))
    t.note_heads = [4, 3, 2]

    assert t.format == "<d' ef' e'>4"


def test_Chord_11():
    '''Set chord note heads to pitches.
    '''

    t = Chord([], (1,4))
    t.note_heads = [pitchtools.NamedChromaticPitch(4), pitchtools.NamedChromaticPitch(3), pitchtools.NamedChromaticPitch(2)]

    assert t.format == "<d' ef' e'>4"


def test_Chord_12():
    '''Set chord note heads to mixed numbers and pitches.
    '''

    t = Chord([], (1,4))
    t.note_heads = [pitchtools.NamedChromaticPitch(4), 3, pitchtools.NamedChromaticPitch(2)]

    assert t.format == "<d' ef' e'>4"


def test_Chord_13():
    '''Set chord item to pitch or number.
    '''

    t = Chord([2, 4], (1,4))
    t[0] = pitchtools.NamedChromaticPitch(5)
    assert t.format == "<e' f'>4"

    t[0] = 7
    assert t.format == "<f' g'>4"
