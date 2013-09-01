# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_PitchSet___slots___01():
    r'''Named chromatic pitch sets are immutable.
    '''

    pitch_classes = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    pitch_set = pitchtools.PitchSet(pitch_classes)

    assert py.test.raises(AttributeError, "pitch_set.foo = 'bar'")
