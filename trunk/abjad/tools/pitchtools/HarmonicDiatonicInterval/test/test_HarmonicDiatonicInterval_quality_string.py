from abjad import *


def test_HarmonicDiatonicInterval_quality_string_01():

    assert pitchtools.HarmonicDiatonicInterval('perfect', 1).quality_string == 'perfect'
    assert pitchtools.HarmonicDiatonicInterval('minor', 2).quality_string == 'minor'
    assert pitchtools.HarmonicDiatonicInterval('major', 2).quality_string == 'major'
    assert pitchtools.HarmonicDiatonicInterval('minor', 3).quality_string == 'minor'
    assert pitchtools.HarmonicDiatonicInterval('major', 3).quality_string == 'major'
    assert pitchtools.HarmonicDiatonicInterval('perfect', 4).quality_string == 'perfect'
    assert pitchtools.HarmonicDiatonicInterval('augmented', 4).quality_string == \
        'augmented'
    assert pitchtools.HarmonicDiatonicInterval('diminished', 5).quality_string == \
        'diminished'
    assert pitchtools.HarmonicDiatonicInterval('perfect', 5).quality_string == 'perfect'
