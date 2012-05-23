from abjad import *


def test_HarmonicDiatonicInterval_melodic_diatonic_interval_ascending_01():

    hdi = pitchtools.HarmonicDiatonicInterval('major', 2)
    mdi = pitchtools.MelodicDiatonicInterval('major', 2)
    assert hdi.melodic_diatonic_interval_ascending == mdi

    hdi = pitchtools.HarmonicDiatonicInterval('major', 9)
    mdi = pitchtools.MelodicDiatonicInterval('major', 9)
    assert hdi.melodic_diatonic_interval_ascending == mdi
