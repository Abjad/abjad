# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_yield_all_pitch_class_sets_01():

    U_star = pitchtools.yield_all_pitch_class_sets()
    assert len(U_star) == 4096
    assert pitchtools.PitchClassSet([0, 1, 2]) in U_star
    assert pitchtools.PitchClassSet([1, 2, 3]) in U_star
    assert pitchtools.PitchClassSet([3, 4, 8, 9, 11]) in U_star
    assert pitchtools.PitchClassSet(range(12)) in U_star
