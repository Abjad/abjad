# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(-3), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('minor', 3)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(-2), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('major', 2)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(-1), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('minor', 2)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(0), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('perfect', 8)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(9), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('minor', 3)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(10), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('major', 2)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(11), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('minor', 2)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(12))
    assert mcpi == pitchtools.NamedIntervalClass('perfect', 1)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-3))
    assert mcpi == pitchtools.NamedIntervalClass('minor', -3)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-2))
    assert mcpi == pitchtools.NamedIntervalClass('major', -2)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(-1))
    assert mcpi == pitchtools.NamedIntervalClass('minor', -2)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(0))
    assert mcpi == pitchtools.NamedIntervalClass('perfect', -8)


def test_pitchtools_NamedIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(9))
    assert mcpi == pitchtools.NamedIntervalClass('minor', -3)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(10))
    assert mcpi == pitchtools.NamedIntervalClass('major', -2)

    mcpi = pitchtools.NamedIntervalClass.from_pitch_carriers(
        NamedPitch(12), NamedPitch(11))
    assert mcpi == pitchtools.NamedIntervalClass('minor', -2)
