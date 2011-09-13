from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitchClassSet


def test_NamedChromaticPitchClassSet___repr___01():
    '''Named chromatic pitch-class set repr is evaluable.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_set_1 = pitchtools.NamedChromaticPitchClassSet(ncpcs)
    named_chromatic_pitch_class_set_2 = eval(repr(named_chromatic_pitch_class_set_1))

    "NamedChromaticPitchClassSet(['a', 'as', 'c', 'cs', 'gs'])"

    assert isinstance(named_chromatic_pitch_class_set_1, pitchtools.NamedChromaticPitchClassSet)
    assert isinstance(named_chromatic_pitch_class_set_2, pitchtools.NamedChromaticPitchClassSet)
