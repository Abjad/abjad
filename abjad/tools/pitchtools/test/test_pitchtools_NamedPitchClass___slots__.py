# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_NamedPitchClass___slots___01():

    named_pitch_class = pitchtools.NamedPitchClass("cs")
    assert pytest.raises(AttributeError, "named_pitch_class.foo = 'bar'")
