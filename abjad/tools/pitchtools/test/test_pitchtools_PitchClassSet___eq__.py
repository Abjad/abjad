# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet___eq___01():
    r'''Named pitch-class set equality works as expected.
    '''

    pitch_class_set_1 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    pitch_class_set_2 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    pitch_class_set_3 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('g'),])

    assert pitch_class_set_1 == pitch_class_set_1
    assert pitch_class_set_1 == pitch_class_set_2
    assert pitch_class_set_1 != pitch_class_set_3
    assert pitch_class_set_2 != pitch_class_set_3


def test_pitchtools_PitchClassSet___eq___02():
    r'''PCset equality works as expected.
    '''

    pitch_class_set_1 = pitchtools.PitchClassSet([0, 2, 6, 7])
    pitch_class_set_2 = pitchtools.PitchClassSet([0, 2, 6, 7])
    pitch_class_set_3 = pitchtools.PitchClassSet([0, 2, 6, 8])

    assert pitch_class_set_1 == pitch_class_set_2
    assert pitch_class_set_1 != pitch_class_set_3
    assert pitch_class_set_2 != pitch_class_set_3
    assert not pitch_class_set_1 != pitch_class_set_2
