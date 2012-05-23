from abjad import *


def test_MelodicDiatonicInterval___eq___01():

    diatonic_interval_1 = pitchtools.MelodicDiatonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.MelodicDiatonicInterval('minor', 2)

    assert diatonic_interval_1 == diatonic_interval_2



def test_MelodicDiatonicInterval___eq___02():

    diatonic_interval_1 = pitchtools.MelodicDiatonicInterval('minor', 2)
    diatonic_interval_2 = pitchtools.MelodicDiatonicInterval('augmented', 1)

    assert not diatonic_interval_1 == diatonic_interval_2
