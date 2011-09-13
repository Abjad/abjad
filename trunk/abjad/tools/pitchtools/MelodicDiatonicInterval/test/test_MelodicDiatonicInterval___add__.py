from abjad import *


def test_MelodicDiatonicInterval___add___01():

    mdi1 = pitchtools.MelodicDiatonicInterval('major', 2)
    mdi2 = pitchtools.MelodicDiatonicInterval('major', 3)
    new = mdi1 + mdi2

    assert new == pitchtools.MelodicDiatonicInterval('augmented', 4)
