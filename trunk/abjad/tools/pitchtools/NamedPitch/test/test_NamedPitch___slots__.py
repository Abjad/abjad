# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitch___slots___01():

    named_pitch = pitchtools.NamedPitch("cs''")
    assert py.test.raises(AttributeError, "named_pitch.foo = 'bar'")
