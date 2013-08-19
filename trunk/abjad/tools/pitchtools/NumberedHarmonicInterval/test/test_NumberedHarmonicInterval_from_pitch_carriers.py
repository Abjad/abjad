# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicInterval_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(15)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(14)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(13)


def test_NumberedHarmonicInterval_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(12)


def test_NumberedHarmonicInterval_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(3)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(2)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(1)


def test_NumberedHarmonicInterval_from_pitch_carriers_04():
    r'''Unison.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert hci == pitchtools.NumberedHarmonicInterval(0)


def test_NumberedHarmonicInterval_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert hci == pitchtools.NumberedHarmonicInterval(15)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert hci == pitchtools.NumberedHarmonicInterval(14)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert hci == pitchtools.NumberedHarmonicInterval(13)


def test_NumberedHarmonicInterval_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert hci == pitchtools.NumberedHarmonicInterval(12)


def test_NumberedHarmonicInterval_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert hci == pitchtools.NumberedHarmonicInterval(3)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert hci == pitchtools.NumberedHarmonicInterval(2)

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert hci == pitchtools.NumberedHarmonicInterval(1)


def test_NumberedHarmonicInterval_from_pitch_carriers_08():
    r'''Works with quartertones.
    '''

    hci = pitchtools.NumberedHarmonicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
    assert hci == pitchtools.NumberedHarmonicInterval(14.5)
