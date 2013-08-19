# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_diatonic_interval_class_01():

    hdi = pitchtools.NamedHarmonicInterval('perfect', 1)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('perfect', 1)

    hdi = pitchtools.NamedHarmonicInterval('minor', 2)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)

    hdi = pitchtools.NamedHarmonicInterval('major', 2)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    hdi = pitchtools.NamedHarmonicInterval('minor', 3)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 3)

    hdi = pitchtools.NamedHarmonicInterval('major', 3)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 3)


def test_NamedHarmonicInterval_diatonic_interval_class_02():

    hdi = pitchtools.NamedHarmonicInterval('perfect', 5)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('perfect', 4)

    hdi = pitchtools.NamedHarmonicInterval('diminished', 5)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('augmented', 4)

    hdi = pitchtools.NamedHarmonicInterval('minor', 6)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 3)

    hdi = pitchtools.NamedHarmonicInterval('minor', 7)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    hdi = pitchtools.NamedHarmonicInterval('major', 7)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)


def test_NamedHarmonicInterval_diatonic_interval_class_03():

    #hdi = pitchtools.NamedHarmonicInterval('perfect', 8)
    #dic = hdi.diatonic_interval_class
    #assert dic == pitchtools.NamedInversionEquivalentIntervalClass('perfect', 8)

    hdi = pitchtools.NamedHarmonicInterval('minor', 9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)

    hdi = pitchtools.NamedHarmonicInterval('major', 9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    hdi = pitchtools.NamedHarmonicInterval('minor', 10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 3)

    hdi = pitchtools.NamedHarmonicInterval('major', 10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 3)


def test_NamedHarmonicInterval_diatonic_interval_class_04():

    #hdi = pitchtools.NamedHarmonicInterval('perfect', -8)
    #dic = hdi.diatonic_interval_class
    #assert dic == pitchtools.NamedInversionEquivalentIntervalClass('perfect', 8)

    hdi = pitchtools.NamedHarmonicInterval('minor', -9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)

    hdi = pitchtools.NamedHarmonicInterval('major', -9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    hdi = pitchtools.NamedHarmonicInterval('minor', -10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 3)

    hdi = pitchtools.NamedHarmonicInterval('major', -10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 3)


def test_NamedHarmonicInterval_diatonic_interval_class_05():

    hdi = pitchtools.NamedHarmonicInterval('perfect', 12)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('perfect', 4)

    hdi = pitchtools.NamedHarmonicInterval('diminished', 12)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('augmented', 4)

    hdi = pitchtools.NamedHarmonicInterval('minor', 13)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 3)

    hdi = pitchtools.NamedHarmonicInterval('minor', 14)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    hdi = pitchtools.NamedHarmonicInterval('major', 14)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)
