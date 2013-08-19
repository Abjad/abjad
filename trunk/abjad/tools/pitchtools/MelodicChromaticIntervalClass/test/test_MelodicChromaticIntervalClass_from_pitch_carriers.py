# -*- encoding: utf-8 -*-
from abjad import *


def test_MelodicChromaticIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(12)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(0)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_MelodicChromaticIntervalClass_from_pitch_carriers_08():
    r'''Quartertones.
    '''

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2.5))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)

    mcic = pitchtools.MelodicChromaticIntervalClass.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9.5))
    assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)
