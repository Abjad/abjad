from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitchClass


def test_NumberedChromaticPitchClass___repr___01():
    '''Numbered chromatic pitch-class repr is evaluable.
    '''

    numbered_chromatic_pitch_class_1 = pitchtools.NumberedChromaticPitchClass(1)
    numbered_chromatic_pitch_class_2 = eval(repr(numbered_chromatic_pitch_class_1))

    assert isinstance(numbered_chromatic_pitch_class_1, pitchtools.NumberedChromaticPitchClass)
    assert isinstance(numbered_chromatic_pitch_class_2, pitchtools.NumberedChromaticPitchClass)
