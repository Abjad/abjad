# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitchClassSet


def test_NumberedPitchClassSet___repr___01():

    numbered_chromatic_pitch_class_set_1 = pitchtools.NumberedPitchClassSet(
        [6, 7, 10, 10.5])
    numbered_chromatic_pitch_class_set_2 = eval(repr(numbered_chromatic_pitch_class_set_1))

    assert isinstance(numbered_chromatic_pitch_class_set_1,
        pitchtools.NumberedPitchClassSet)
    assert isinstance(numbered_chromatic_pitch_class_set_2,
        pitchtools.NumberedPitchClassSet)
