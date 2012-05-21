from abjad import *


def testMelodicObjectDiatonicInterval___neg___01():

    interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    assert -interval == pitchtools.MelodicDiatonicInterval('minor', -3)


def testMelodicObjectDiatonicInterval___neg___02():

    interval = pitchtools.MelodicDiatonicInterval('minor', -3)
    assert -interval == pitchtools.MelodicDiatonicInterval('minor', 3)
