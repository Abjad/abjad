from abjad import *
from abjad.tools.pitchtools import NumberedDiatonicPitchClass


def test_NumberedDiatonicPitchClass___repr___01():
    '''Numbered diatonic pitch-class repr is evaluable.
    '''

    numbered_diatonic_pitch_class_1 = pitchtools.NumberedDiatonicPitchClass(0)
    numbered_diatonic_pitch_class_2 = eval(repr(numbered_diatonic_pitch_class_1))

    assert isinstance(numbered_diatonic_pitch_class_1, pitchtools.NumberedDiatonicPitchClass)
    assert isinstance(numbered_diatonic_pitch_class_2, pitchtools.NumberedDiatonicPitchClass)
