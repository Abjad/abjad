# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_harmonic_diatonic_interval_class_01():

    diatonic_interval = pitchtools.NamedHarmonicInterval('perfect', 1)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 1
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('perfect', 1)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', 2)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', 2)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', 3)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', 3)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 3)


def test_NamedHarmonicInterval_harmonic_diatonic_interval_class_02():

    diatonic_interval = pitchtools.NamedHarmonicInterval('perfect', 8)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 1
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('perfect', 8)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', 9)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', 9)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', 10)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', 10)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 3)


def test_NamedHarmonicInterval_harmonic_diatonic_interval_class_03():

    diatonic_interval = pitchtools.NamedHarmonicInterval('perfect', -8)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 1
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('perfect', 8)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', -9)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', -9)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 2
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedHarmonicInterval('minor', -10)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedHarmonicInterval('major', -10)
    #assert diatonic_interval.harmonic_diatonic_interval_class == 3
    ic = diatonic_interval.harmonic_diatonic_interval_class
    assert ic == pitchtools.NamedHarmonicIntervalClass('major', 3)
