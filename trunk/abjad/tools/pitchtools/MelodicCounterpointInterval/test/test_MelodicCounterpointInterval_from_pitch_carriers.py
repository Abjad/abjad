# -*- encoding: utf-8 -*-
from abjad import *


def test_MelodicCounterpointInterval_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(10)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(9)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(9)


def test_MelodicCounterpointInterval_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(8)


def test_MelodicCounterpointInterval_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(3)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(2)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(2)


def test_MelodicCounterpointInterval_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert mcpi == pitchtools.MelodicCounterpointInterval(1)


def test_MelodicCounterpointInterval_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-10)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-9)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-9)


def test_MelodicCounterpointInterval_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-8)


def test_MelodicCounterpointInterval_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-3)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-2)

    mcpi = pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert mcpi == pitchtools.MelodicCounterpointInterval(-2)
