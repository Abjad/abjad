# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_01():

    pitch = pitchtools.NamedPitch(12)

    diatonic_interval = pitchtools.NamedInterval('minor', 2)
    transposed = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, diatonic_interval)

    assert transposed == pitchtools.NamedPitch('df', 5)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_02():

    pitch = pitchtools.NamedPitch(12)

    chromatic_interval = pitchtools.NumberedInterval(1)
    transposed = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, chromatic_interval)

    assert transposed == pitchtools.NamedPitch('cs', 5)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_03():
    r'''Transpose pitch.
    '''

    pitch = pitchtools.NamedPitch(12)
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, interval)
    assert new == pitchtools.NamedPitch(9)
    assert new is not pitch


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_04():
    r'''Transpose note.
    '''

    note = Note(12, (1, 4))
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(note, interval)
    assert new.written_pitch == pitchtools.NamedPitch(9)
    assert new is not note


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_05():
    r'''Transpose chord.
    '''

    chord = Chord([12, 13, 14], (1, 4))
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_melodic_interval(chord, interval)
    assert new.written_pitches == tuple([pitchtools.NamedPitch(x) for x in [9, 10, 11]])
    assert new is not chord


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_06():

    pitch = pitchtools.NamedPitch(12)
    mdi = pitchtools.NamedInterval('minor', -3)

    transposed_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, mdi)
    assert transposed_pitch == pitchtools.NamedPitch('a', 4)


def test_pitchtools_transpose_pitch_carrier_by_melodic_interval_07():
    r'''Retun non-pitch-carrying input changed.
    '''

    rest = Rest('r4')

    assert pitchtools.transpose_pitch_carrier_by_melodic_interval(rest, '+m2') is rest
