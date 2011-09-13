from abjad import *


def test_MelodicDiatonicInterval_quality_string_01():

    assert pitchtools.MelodicDiatonicInterval('perfect', 1).quality_string == \
        'perfect'
    assert pitchtools.MelodicDiatonicInterval('minor', 2).quality_string == \
        'minor'
    assert pitchtools.MelodicDiatonicInterval('major', 2).quality_string == \
        'major'
    assert pitchtools.MelodicDiatonicInterval('minor', 3).quality_string == \
        'minor'
    assert pitchtools.MelodicDiatonicInterval('major', 3).quality_string == \
        'major'
    assert pitchtools.MelodicDiatonicInterval('perfect', 4).quality_string == \
        'perfect'
    assert pitchtools.MelodicDiatonicInterval('augmented', 4).quality_string == \
        'augmented'
    assert pitchtools.MelodicDiatonicInterval('diminished', 5).quality_string ==\
        'diminished'
    assert pitchtools.MelodicDiatonicInterval('perfect', 5).quality_string == \
        'perfect'
