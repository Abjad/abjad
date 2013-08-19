# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment___add___01():
    r'''Adding numbered chromatic pitch-class segments returns
    a new numbered chromatic pitch-class segment.
    '''

    a = pitchtools.NumberedPitchClassSegment([0, 1, 2])
    b = pitchtools.NumberedPitchClassSegment([3, 4, 5])

    assert a + b == pitchtools.NumberedPitchClassSegment([0, 1, 2, 3, 4, 5])
