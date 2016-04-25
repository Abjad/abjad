# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import PitchClassSet


def test_pitchtools_PitchClassSet___repr___01():
    r'''Named pitch-class set repr is evaluable.
    '''

    named_pitch_classes = ['gs', 'a', 'as', 'c', 'cs']
    named_pitch_class_set_1 = pitchtools.PitchClassSet(named_pitch_classes)
    named_pitch_class_set_2 = eval(repr(named_pitch_class_set_1))

    "PitchClassSet(['a', 'as', 'c', 'cs', 'gs'])"

    assert isinstance(named_pitch_class_set_1, pitchtools.PitchClassSet)
    assert isinstance(named_pitch_class_set_2, pitchtools.PitchClassSet)


def test_pitchtools_PitchClassSet___repr___02():

    numbered_pitch_class_set_1 = pitchtools.PitchClassSet(
        [6, 7, 10, 10.5])
    numbered_pitch_class_set_2 = eval(repr(numbered_pitch_class_set_1))

    assert isinstance(numbered_pitch_class_set_1,
        pitchtools.PitchClassSet)
    assert isinstance(numbered_pitch_class_set_2,
        pitchtools.PitchClassSet)
