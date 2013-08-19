# -*- encoding: utf-8 -*-
from abjad import *


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)
