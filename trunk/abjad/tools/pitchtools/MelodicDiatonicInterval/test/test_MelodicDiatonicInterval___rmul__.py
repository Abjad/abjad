from abjad import *


def test_MelodicDiatonicInterval___rmul___01():

    major_second = pitchtools.MelodicDiatonicInterval('major', 2)

    assert 0 * major_second == pitchtools.MelodicDiatonicInterval('perfect', 1)
    assert 1 * major_second == pitchtools.MelodicDiatonicInterval('major', 2)
    assert 2 * major_second == pitchtools.MelodicDiatonicInterval('major', 3)
    assert 3 * major_second == pitchtools.MelodicDiatonicInterval('augmented', 4)
