# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_PitchClassSet___slots___01():
    r'''Named pitch-class set can not be changed after initialization.
    '''

    named_pitch_classes = ['gs', 'a', 'as', 'c', 'cs']
    named_pitch_class_set = pitchtools.PitchClassSet(named_pitch_classes)

    assert pytest.raises(AttributeError,
        "named_pitch_class_set.foo = 'bar'")
