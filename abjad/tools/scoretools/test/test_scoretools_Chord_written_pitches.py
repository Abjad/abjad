# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Chord_written_pitches_01():
    r'''Returns immutable tuple of pitches in chord.
    '''

    chord = Chord("<d' e' f'>4")
    pitches = chord.written_pitches

    assert isinstance(pitches, pitchtools.PitchSegment)
    assert len(pitches) == 3
    assert pytest.raises(Exception, 'pitches.pop()')
    assert pytest.raises(Exception, 'pitches.remove(pitches[0])')


def test_scoretools_Chord_written_pitches_02():
    r'''Equivalent written pitches compare equal.
    '''

    chord_1 = Chord("<d' e' f'>4")
    chord_2 = Chord("<d' e' f'>4")

    assert chord_1.written_pitches == chord_2.written_pitches


def test_scoretools_Chord_written_pitches_03():
    '''Transpose sounding pitches to written pitches.
    '''

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()
    attach(glockenspiel, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        ''')

    assert staff[0].written_pitches == (
        NamedPitch("c'"),
        NamedPitch("e'"),
        )


def test_scoretools_Chord_written_pitches_04():
    r'''Set written pitches with pitch numbers.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [4, 3, 2]
    assert format(chord) == "<d' ef' e'>4"

    chord.written_pitches = (4, 3, 2)
    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord_written_pitches_05():
    r'''Set written pitches with pitches.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [
        NamedPitch(4),
        NamedPitch(3),
        NamedPitch(2),
        ]

    assert format(chord) == "<d' ef' e'>4"


def test_scoretools_Chord_written_pitches_06():
    r'''Set written pitches with both pitches and pitch numbers.
    '''

    chord = Chord([], (1, 4))
    chord.written_pitches = [
        4,
        NamedPitch(3),
        NamedPitch(2),
        ]

    assert format(chord) == "<d' ef' e'>4"
