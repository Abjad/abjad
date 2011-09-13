from abjad import *


def test_NumberedChromaticPitchClassSegment_alpha_01():
    '''Morris alpha transform of numbered chromatic pitch-class segment.
    '''

    ncpcs = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    assert ncpcs.alpha() == pitchtools.NumberedChromaticPitchClassSegment([1, 7, 11, 5, 8, 3])
