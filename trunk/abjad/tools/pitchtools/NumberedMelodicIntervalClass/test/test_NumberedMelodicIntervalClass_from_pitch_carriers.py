# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(3)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(2)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(1)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(12)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(3)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(2)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(1)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(0)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-3)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-2)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-1)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-12)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-3)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-2)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-1)


def test_NumberedMelodicIntervalClass_from_pitch_carriers_08():
    r'''Quartertones.
    '''

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-2.5)

    mcic = pitchtools.NumberedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9.5))
    assert mcic == pitchtools.NumberedMelodicIntervalClass(-2.5)
