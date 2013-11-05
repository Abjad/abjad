# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_NamedPitch___slots___01():

    named_pitch = pitchtools.NamedPitch("cs''")
    assert pytest.raises(AttributeError, "named_pitch.foo = 'bar'")
