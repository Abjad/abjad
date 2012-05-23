from abjad import *


def test_MelodicDiatonicInterval___neg___01():

    interval = pitchtools.MelodicDiatonicInterval('minor', 3)
    assert -interval == pitchtools.MelodicDiatonicInterval('minor', -3)


def test_MelodicDiatonicInterval___neg___02():

    interval = pitchtools.MelodicDiatonicInterval('minor', -3)
    assert -interval == pitchtools.MelodicDiatonicInterval('minor', 3)
