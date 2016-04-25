# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet___init___01():
    r'''Initialize with named pitch-classes.
    '''

    named_pitch_class_set = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e')])

    assert len(named_pitch_class_set) == 3


def test_pitchtools_PitchClassSet___init___02():
    r'''Works with numbers.
    '''

    assert len(pitchtools.PitchClassSet([0, 2, 6, 7])) == 4


def test_pitchtools_PitchClassSet___init___03():
    r'''Works with pitch-classes.
    '''

    assert len(pitchtools.PitchClassSet(
        [pitchtools.NumberedPitchClass(x) for x in [0, 2, 6, 7]])) == 4
