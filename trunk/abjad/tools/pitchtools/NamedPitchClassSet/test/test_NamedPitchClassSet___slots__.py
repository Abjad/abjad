# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitchClassSet___slots___01():
    r'''Named chromatic pitch-class set can not be changed after initialization.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_set = pitchtools.NamedPitchClassSet(ncpcs)

    assert py.test.raises(AttributeError, "named_chromatic_pitch_class_set.foo = 'bar'")
