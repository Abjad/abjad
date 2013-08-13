# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Chord_written_pitches_01():
    r'''Returns immutable tuple of pitches in chord.
    '''

    chord = Chord("<d' e' f'>4")
    pitches = chord.written_pitches

    assert isinstance(pitches, tuple)
    assert len(pitches) == 3
    assert py.test.raises(Exception, 'pitches.pop()')
    assert py.test.raises(Exception, 'pitches.remove(pitches[0])')


def test_Chord_written_pitches_02():
    r'''Equivalent written pitches compare equal.
    '''

    chord_1 = Chord("<d' e' f'>4")
    chord_2 = Chord("<d' e' f'>4")

    assert chord_1.written_pitches == chord_2.written_pitches


def test_Chord_written_pitches_03():
    '''Transpose sounding pitches to written pitches.
    '''

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()(staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        ''')

    assert staff[0].written_pitches == (
        pitchtools.NamedChromaticPitch("c'"), 
        pitchtools.NamedChromaticPitch("e'"),
        )


def test_Chord_written_pitches_04():
    r'''Set written pitches with pitch numbers.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [4, 3, 2]
    assert chord.lilypond_format == "<d' ef' e'>4"

    chord.written_pitches = (4, 3, 2)
    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_written_pitches_05():
    r'''Set written pitches with pitches.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [
        pitchtools.NamedChromaticPitch(4), 
        pitchtools.NamedChromaticPitch(3),
        pitchtools.NamedChromaticPitch(2),
        ]

    assert chord.lilypond_format == "<d' ef' e'>4"


def test_Chord_written_pitches_06():
    r'''Set written pitches with both pitches and pitch numbers.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [
        4, 
        pitchtools.NamedChromaticPitch(3), 
        pitchtools.NamedChromaticPitch(2),
        ]

    assert chord.lilypond_format == "<d' ef' e'>4"
