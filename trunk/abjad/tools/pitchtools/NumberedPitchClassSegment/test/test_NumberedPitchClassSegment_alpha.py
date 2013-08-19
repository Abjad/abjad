# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment_alpha_01():
    r'''Morris alpha transform of numbered chromatic pitch-class segment.
    '''

    ncpcs = pitchtools.NumberedPitchClassSegment([0, 6, 10, 4, 9, 2])
    assert ncpcs.alpha() == pitchtools.NumberedPitchClassSegment([1, 7, 11, 5, 8, 3])
