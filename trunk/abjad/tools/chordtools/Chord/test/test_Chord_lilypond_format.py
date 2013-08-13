from abjad import *


def test_Chord_lilypond_format_01():
    r'''Format chord with one note head.
    '''

    chord = Chord("<cqs'>4")

    assert str(chord) == "<cqs'>4"
    assert chord.lilypond_format == "<cqs'>4"
    assert len(chord) == 1
    assert len(chord.note_heads) == 1
    assert len(chord.written_pitches) == 1


def test_Chord_lilypond_format_02():
    r'''Format chord with LilyPond command mark.
    '''

    chord = Chord("<d' ef' e'>4")
    marktools.LilyPondCommandMark('glissando', 'right')(chord)

    assert chord.lilypond_format == "<d' ef' e'>4 \\glissando"


def test_Chord_lilypond_format_03():
    r'''Format tweaked chord with LilyPond command mark.
    '''

    chord = Chord("<d' ef' e'>4")
    chord[0].tweak.color = 'red'
    marktools.LilyPondCommandMark('glissando', 'right')(chord)

    assert testtools.compare(
        chord,
        r'''
        <
            \tweak #'color #red
            d'
            ef'
            e'
        >4 \glissando
        '''
        )

    assert select(chord).is_well_formed()
