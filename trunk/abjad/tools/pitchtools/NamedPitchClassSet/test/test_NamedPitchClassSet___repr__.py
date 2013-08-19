# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitchClassSet


def test_NamedPitchClassSet___repr___01():
    r'''Named chromatic pitch-class set repr is evaluable.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_set_1 = pitchtools.NamedPitchClassSet(ncpcs)
    named_chromatic_pitch_class_set_2 = eval(repr(named_chromatic_pitch_class_set_1))

    "NamedPitchClassSet(['a', 'as', 'c', 'cs', 'gs'])"

    assert isinstance(named_chromatic_pitch_class_set_1, pitchtools.NamedPitchClassSet)
    assert isinstance(named_chromatic_pitch_class_set_2, pitchtools.NamedPitchClassSet)
