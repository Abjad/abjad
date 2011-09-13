from abjad import *


def test_MelodicDiatonicInterval___abs___01():

    interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)


def test_MelodicDiatonicInterval___abs___02():

    interval = pitchtools.MelodicDiatonicInterval('minor', -3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)
