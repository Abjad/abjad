from abjad import *


def testHarmonicObjectDiatonicInterval_melodic_diatonic_interval_descending_01():

    hdi = pitchtools.HarmonicDiatonicInterval('major', 2)
    mdi = pitchtools.MelodicDiatonicInterval('major', -2)
    assert hdi.melodic_diatonic_interval_descending == mdi

    hdi = pitchtools.HarmonicDiatonicInterval('major', 9)
    mdi = pitchtools.MelodicDiatonicInterval('major', -9)
    assert hdi.melodic_diatonic_interval_descending == mdi
