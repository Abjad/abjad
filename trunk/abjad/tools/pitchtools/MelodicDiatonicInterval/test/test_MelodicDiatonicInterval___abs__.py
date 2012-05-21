from abjad import *


def testMelodicObjectDiatonicInterval___abs___01():

    interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)


def testMelodicObjectDiatonicInterval___abs___02():

    interval = pitchtools.MelodicDiatonicInterval('minor', -3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)
