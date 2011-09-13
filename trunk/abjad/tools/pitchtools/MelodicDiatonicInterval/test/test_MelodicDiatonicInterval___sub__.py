from abjad import *


def test_MelodicDiatonicInterval___sub___01():

    major_second_ascending = pitchtools.MelodicDiatonicInterval('major', 2)
    major_third_ascending = pitchtools.MelodicDiatonicInterval('major', 3)

    difference = major_second_ascending - major_third_ascending
    assert difference == pitchtools.MelodicDiatonicInterval('major', -2)

    difference = major_third_ascending - major_second_ascending
    assert difference == pitchtools.MelodicDiatonicInterval('major', 2)

    difference = major_second_ascending - major_second_ascending
    assert difference == pitchtools.MelodicDiatonicInterval('perfect', 1)

    difference = major_third_ascending - major_third_ascending
    assert difference == pitchtools.MelodicDiatonicInterval('perfect', 1)
