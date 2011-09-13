from abjad import *
from abjad.tools.pitchtools import NamedDiatonicPitchClass


def test_NamedDiatonicPitchClass___repr___01():
    '''Named diatonic pitch-class repr is evaluable.
    '''

    named_diatonic_pitch_class_1 = pitchtools.NamedDiatonicPitchClass('c')
    named_diatonic_pitch_class_2 = eval(repr(named_diatonic_pitch_class_1))

    assert isinstance(named_diatonic_pitch_class_1, pitchtools.NamedDiatonicPitchClass)
    assert isinstance(named_diatonic_pitch_class_2, pitchtools.NamedDiatonicPitchClass)
