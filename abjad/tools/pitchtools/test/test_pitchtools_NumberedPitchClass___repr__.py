# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitchClass


def test_pitchtools_NumberedPitchClass___repr___01():
    r'''Numbered pitch-class repr is evaluable.
    '''

    numbered_pitch_class_1 = pitchtools.NumberedPitchClass(1)
    numbered_pitch_class_2 = eval(repr(numbered_pitch_class_1))

    assert isinstance(numbered_pitch_class_1, pitchtools.NumberedPitchClass)
    assert isinstance(numbered_pitch_class_2, pitchtools.NumberedPitchClass)
