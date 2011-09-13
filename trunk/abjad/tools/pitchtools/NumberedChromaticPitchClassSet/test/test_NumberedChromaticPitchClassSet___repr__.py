from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitchClassSet


def test_NumberedChromaticPitchClassSet___repr___01():

    numbered_chromatic_pitch_class_set_1 = pitchtools.NumberedChromaticPitchClassSet(
        [6, 7, 10, 10.5])
    numbered_chromatic_pitch_class_set_2 = eval(repr(numbered_chromatic_pitch_class_set_1))

    assert isinstance(numbered_chromatic_pitch_class_set_1,
        pitchtools.NumberedChromaticPitchClassSet)
    assert isinstance(numbered_chromatic_pitch_class_set_2,
        pitchtools.NumberedChromaticPitchClassSet)
