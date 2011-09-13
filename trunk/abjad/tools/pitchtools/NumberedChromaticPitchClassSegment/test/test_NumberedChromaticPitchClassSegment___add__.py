from abjad import *


def test_NumberedChromaticPitchClassSegment___add___01():
    '''Adding numbered chromatic pitch-class segments returns
    a new numbered chromatic pitch-class segment.
    '''

    a = pitchtools.NumberedChromaticPitchClassSegment([0, 1, 2])
    b = pitchtools.NumberedChromaticPitchClassSegment([3, 4, 5])

    assert a + b == pitchtools.NumberedChromaticPitchClassSegment([0, 1, 2, 3, 4, 5])
