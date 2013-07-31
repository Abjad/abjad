# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_calculate_harmonic_chromatic_interval_class_01():
    r'''Ascending intervals greater than an octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(-3), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(-1), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_02():
    r'''Ascending octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_03():
    r'''Ascending intervals less than an octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(9), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(10), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(11), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_04():
    r'''Unison.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(12))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_05():
    r'''Descending intervals greater than an octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-3))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-1))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_06():
    r'''Descending octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(0))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_07():
    r'''Descending intervals less than an octave.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(9))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(10))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(11))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_08():
    r'''Works with quartertones.
    '''

    hcic = pitchtools.calculate_harmonic_chromatic_interval_class(
        pitchtools.NamedChromaticPitch(12), pitchtools.NamedChromaticPitch(-2.5))
    assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
