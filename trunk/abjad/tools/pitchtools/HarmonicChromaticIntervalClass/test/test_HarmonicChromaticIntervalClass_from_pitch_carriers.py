# -*- encoding: utf-8 -*-
from abjad import *


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_HarmonicChromaticIntervalClass_from_pitch_carriers_08():
    r'''Works with quartertones.
    '''

    hcic = pitchtools.HarmonicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
