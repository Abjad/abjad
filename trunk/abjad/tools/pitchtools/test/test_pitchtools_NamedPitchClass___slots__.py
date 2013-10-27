# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_NamedPitchClass___slots___01():

    named_pitch_class = pitchtools.NamedPitchClass("cs")
    assert py.test.raises(AttributeError, "named_pitch_class.foo = 'bar'")
