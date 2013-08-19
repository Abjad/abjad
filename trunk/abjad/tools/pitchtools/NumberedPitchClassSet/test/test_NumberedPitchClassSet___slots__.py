# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitchClassSet___slots___01():
    r'''Numbered chromatic pitch-class sets are immutable.
    '''

    numbered_chromatic_pitch_class_set = pitchtools.NumberedPitchClassSet([6, 7, 10, 10.5])
    assert py.test.raises(AttributeError, "numbered_chromatic_pitch_class_set.foo = 'bar'")
