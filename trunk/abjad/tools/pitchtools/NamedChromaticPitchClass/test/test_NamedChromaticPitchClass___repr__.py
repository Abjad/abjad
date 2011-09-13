from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitchClass


def test_NamedChromaticPitchClass___repr___01():
    '''Named chromatic pitch-class repr is evaluable.
    '''

    named_chromatic_pitch_class_1 = pitchtools.NamedChromaticPitchClass('cs')
    named_chromatic_pitch_class_2 = eval(repr(named_chromatic_pitch_class_1))

    "NamedChromaticPitchClass('cs')"

    assert isinstance(named_chromatic_pitch_class_1, pitchtools.NamedChromaticPitchClass)
    assert isinstance(named_chromatic_pitch_class_2, pitchtools.NamedChromaticPitchClass)
