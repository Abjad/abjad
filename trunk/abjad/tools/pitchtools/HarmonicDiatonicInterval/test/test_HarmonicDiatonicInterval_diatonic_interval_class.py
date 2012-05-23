from abjad import *


def test_HarmonicDiatonicInterval_diatonic_interval_class_01():

    hdi = pitchtools.HarmonicDiatonicInterval('perfect', 1)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 1)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 2)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 2)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 3)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 3)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)


def test_HarmonicDiatonicInterval_diatonic_interval_class_02():

    hdi = pitchtools.HarmonicDiatonicInterval('perfect', 5)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 4)

    hdi = pitchtools.HarmonicDiatonicInterval('diminished', 5)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 4)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 6)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 7)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 7)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)


def test_HarmonicDiatonicInterval_diatonic_interval_class_03():

    #hdi = pitchtools.HarmonicDiatonicInterval('perfect', 8)
    #dic = hdi.diatonic_interval_class
    #assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 8)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)


def test_HarmonicDiatonicInterval_diatonic_interval_class_04():

    #hdi = pitchtools.HarmonicDiatonicInterval('perfect', -8)
    #dic = hdi.diatonic_interval_class
    #assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 8)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', -9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('major', -9)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', -10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3)

    hdi = pitchtools.HarmonicDiatonicInterval('major', -10)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)


def test_HarmonicDiatonicInterval_diatonic_interval_class_05():

    hdi = pitchtools.HarmonicDiatonicInterval('perfect', 12)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 4)

    hdi = pitchtools.HarmonicDiatonicInterval('diminished', 12)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 4)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 13)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)

    hdi = pitchtools.HarmonicDiatonicInterval('minor', 14)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)

    hdi = pitchtools.HarmonicDiatonicInterval('major', 14)
    dic = hdi.diatonic_interval_class
    assert dic == pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)
