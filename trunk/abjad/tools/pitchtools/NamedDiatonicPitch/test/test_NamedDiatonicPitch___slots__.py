# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedDiatonicPitch___slots___01():
    r'''Named diatonic pitches are immutable.
    '''

    named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")
    assert py.test.raises(AttributeError, "named_diatonic_pitch.foo = 'bar'")
