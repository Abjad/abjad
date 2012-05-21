from abjad import *


def testHarmonicObjectDiatonicInterval___abs___01():

    interval = pitchtools.HarmonicDiatonicInterval('minor', 3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)


def testHarmonicObjectDiatonicInterval___abs___02():

    interval = pitchtools.HarmonicDiatonicInterval('minor', -3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)
