# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 2)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('perfect', 8)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 2)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('perfect', 1)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 2)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('perfect', 8)


def test_NamedHarmonicIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    hdic = pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert hdic == pitchtools.NamedHarmonicIntervalClass('minor', 2)
