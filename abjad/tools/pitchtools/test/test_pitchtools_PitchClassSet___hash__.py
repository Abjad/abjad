# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet___hash___01():
    r'''Named pitch-class sets are hashable.
    '''

    named_pitch_class_set = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    assert hash(named_pitch_class_set) == hash(repr(named_pitch_class_set))


def test_pitchtools_PitchClassSet___hash___02():
    r'''Pitch class sets are hashable.
    '''

    pitch_class_set = pitchtools.PitchClassSet([0, 1, 2])

    assert hash(pitch_class_set) == hash(repr(pitch_class_set))
