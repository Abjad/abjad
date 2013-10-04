# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitchClass


def test_NamedPitchClass___repr___01():
    r'''Named chromatic pitch-class repr is evaluable.
    '''

    named_pitch_class_1 = pitchtools.NamedPitchClass('cs')
    named_pitch_class_2 = eval(repr(named_pitch_class_1))

    "NamedPitchClass('cs')"

    assert isinstance(named_pitch_class_1, pitchtools.NamedPitchClass)
    assert isinstance(named_pitch_class_2, pitchtools.NamedPitchClass)
