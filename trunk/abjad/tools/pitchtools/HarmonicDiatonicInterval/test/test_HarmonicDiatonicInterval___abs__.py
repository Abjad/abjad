from abjad import *


def test_HarmonicDiatonicInterval___abs___01():

    interval = pitchtools.HarmonicDiatonicInterval('minor', 3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)


def test_HarmonicDiatonicInterval___abs___02():

    interval = pitchtools.HarmonicDiatonicInterval('minor', -3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)
