from abjad import *


def test_HarmonicDiatonicInterval_compare_01():
    '''Compare on interval numbers when interval numbers differ.'''

    hdi_1 = pitchtools.HarmonicDiatonicInterval('major', 2)
    hdi_2 = pitchtools.HarmonicDiatonicInterval('major', 3)

    assert not hdi_1 >  hdi_2
    assert not hdi_1 >=  hdi_2
    assert      hdi_1 <  hdi_2
    assert      hdi_1 <= hdi_2


def test_HarmonicDiatonicInterval_compare_02():
    '''Compare on semitones numbers when interval numbers are equal.'''

    hdi_1 = pitchtools.HarmonicDiatonicInterval('augmented', 2)
    hdi_2 = pitchtools.HarmonicDiatonicInterval('minor', 3)

    assert not hdi_1 >  hdi_2
    assert not hdi_1 >=  hdi_2
    assert      hdi_1 <  hdi_2
    assert      hdi_1 <= hdi_2
