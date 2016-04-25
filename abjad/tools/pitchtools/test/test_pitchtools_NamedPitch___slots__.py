# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NamedPitch___slots___01():

    named_pitch = NamedPitch("cs''")
    assert pytest.raises(AttributeError, "named_pitch.foo = 'bar'")
