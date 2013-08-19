# -*- encoding: utf-8 -*-
from abjad import *


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_HarmonicDiatonicIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

    hdic = pitchtools.HarmonicDiatonicIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)
