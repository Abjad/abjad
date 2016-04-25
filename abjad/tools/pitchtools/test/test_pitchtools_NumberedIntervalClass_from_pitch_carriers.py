# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(-3), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(3)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(-2), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(2)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(-1), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(1)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(0), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(12)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(9), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(3)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(10), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(2)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(11), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(1)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(12))
    assert mcic == pitchtools.NumberedIntervalClass(0)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-3))
    assert mcic == pitchtools.NumberedIntervalClass(-3)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-2))
    assert mcic == pitchtools.NumberedIntervalClass(-2)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-1))
    assert mcic == pitchtools.NumberedIntervalClass(-1)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(0))
    assert mcic == pitchtools.NumberedIntervalClass(-12)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(9))
    assert mcic == pitchtools.NumberedIntervalClass(-3)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(10))
    assert mcic == pitchtools.NumberedIntervalClass(-2)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(11))
    assert mcic == pitchtools.NumberedIntervalClass(-1)


def test_pitchtools_NumberedIntervalClass_from_pitch_carriers_08():
    r'''Quartertones.
    '''

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-2.5))
    assert mcic == pitchtools.NumberedIntervalClass(-2.5)

    mcic = pitchtools.NumberedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(9.5))
    assert mcic == pitchtools.NumberedIntervalClass(-2.5)
