# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NamedPitchClass___slots___01():

    named_pitch_class = pitchtools.NamedPitchClass("cs")
    assert pytest.raises(AttributeError, "named_pitch_class.foo = 'bar'")
