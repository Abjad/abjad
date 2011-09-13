from abjad import *


def test_HarmonicDiatonicInterval___eq___01():

    diatonic_interval_1 = pitchtools.HarmonicDiatonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.HarmonicDiatonicInterval('minor', 2)

    assert diatonic_interval_1 == diatonic_interval_2


def test_HarmonicDiatonicInterval___eq___02():

    diatonic_interval_1 = pitchtools.HarmonicDiatonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.HarmonicDiatonicInterval('augmented', 1)

    assert not diatonic_interval_1 == diatonic_interval_2
