# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Chord_written_pitches_01():
    r'''Returns immutable tuple of pitches in chord.
    '''

    chord = Chord([2, 4, 5], (1, 4))
    pitches = chord.written_pitches

    assert isinstance(pitches, tuple)
    assert len(pitches) == 3
    assert py.test.raises(AttributeError, 'pitches.pop()')
    assert py.test.raises(AttributeError, 'pitches.remove(pitches[0])')


def test_Chord_written_pitches_02():
    r'''Chords with equivalent numbers carry equivalent pitches.
    '''

    t1 = Chord([2, 4, 5], (1, 4))
    t2 = Chord([2, 4, 5], (1, 4))

    assert t1.written_pitches == t2.written_pitches


def test_Chord_written_pitches_03():

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()(staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Glockenspiel }
        \set Staff.shortInstrumentName = \markup { Gkspl. }
        <c' e'>4
        <d' fs'>4
    }
    '''

    assert staff[0].written_pitches == (
        pitchtools.NamedChromaticPitch("c'"), 
        pitchtools.NamedChromaticPitch("e'"),
        )
