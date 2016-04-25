# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_transpose_pitch_carrier_by_interval_01():

    pitch = NamedPitch(12)

    named_interval = pitchtools.NamedInterval('minor', 2)
    transposed = pitchtools.transpose_pitch_carrier_by_interval(pitch, named_interval)

    assert transposed == NamedPitch('df', 5)


def test_pitchtools_transpose_pitch_carrier_by_interval_02():

    pitch = NamedPitch(12)

    numbered_interval = pitchtools.NumberedInterval(1)
    transposed = pitchtools.transpose_pitch_carrier_by_interval(pitch, numbered_interval)

    assert transposed == NamedPitch('cs', 5)


def test_pitchtools_transpose_pitch_carrier_by_interval_03():
    r'''Transpose pitch.
    '''

    pitch = NamedPitch(12)
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_interval(pitch, interval)
    assert new == NamedPitch(9)
    assert new is not pitch


def test_pitchtools_transpose_pitch_carrier_by_interval_04():
    r'''Transpose note.
    '''

    note = Note(12, (1, 4))
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_interval(note, interval)
    assert new.written_pitch == NamedPitch(9)
    assert new is not note


def test_pitchtools_transpose_pitch_carrier_by_interval_05():
    r'''Transpose chord.
    '''

    chord = Chord([12, 13, 14], (1, 4))
    interval = pitchtools.NumberedInterval(-3)
    new = pitchtools.transpose_pitch_carrier_by_interval(chord, interval)
    assert new.written_pitches == tuple([NamedPitch(x) for x in [9, 10, 11]])
    assert new is not chord


def test_pitchtools_transpose_pitch_carrier_by_interval_06():

    pitch = NamedPitch(12)
    mdi = pitchtools.NamedInterval('minor', -3)

    transposed_pitch = pitchtools.transpose_pitch_carrier_by_interval(pitch, mdi)
    assert transposed_pitch == NamedPitch('a', 4)


def test_pitchtools_transpose_pitch_carrier_by_interval_07():
    r'''Retun non-pitch-carrying input changed.
    '''

    rest = Rest('r4')

    assert pitchtools.transpose_pitch_carrier_by_interval(rest, '+m2') is rest
