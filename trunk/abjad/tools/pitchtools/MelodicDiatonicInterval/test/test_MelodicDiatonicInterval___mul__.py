from abjad import *


def test_MelodicDiatonicInterval___mul___01():

    major_second = pitchtools.MelodicDiatonicInterval('major', 2)

    assert major_second * 0 == pitchtools.MelodicDiatonicInterval('perfect', 1)
    assert major_second * 1 == pitchtools.MelodicDiatonicInterval('major', 2)
    assert major_second * 2 == pitchtools.MelodicDiatonicInterval('major', 3)
    assert major_second * 3 == pitchtools.MelodicDiatonicInterval('augmented', 4)


def test_MelodicDiatonicInterval___mul___02():
    '''Negative multiplicands work correctly.
    '''

    ascending_major_second = pitchtools.MelodicDiatonicInterval('+m2')
    descending_major_second = pitchtools.MelodicDiatonicInterval('-m2')

    assert ascending_major_second * -1 == descending_major_second
    assert descending_major_second * -1 == ascending_major_second
