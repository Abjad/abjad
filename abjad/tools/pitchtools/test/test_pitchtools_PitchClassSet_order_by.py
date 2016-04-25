# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet_order_by_01():

    named_pitch_class_set = pitchtools.PitchClassSet(['c', 'e', 'b'])
    named_pitch_class_segment = pitchtools.PitchClassSegment(['e', 'a', 'f'])
    ordered_set = named_pitch_class_set.order_by(
        named_pitch_class_segment)

    assert ordered_set == pitchtools.PitchClassSegment(['b', 'e', 'c'])
