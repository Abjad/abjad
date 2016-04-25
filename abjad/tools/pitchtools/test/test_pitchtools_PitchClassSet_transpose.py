# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet_transpose_01():

    pitch_class_set_1 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    pitch_class_set_2 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('df'),
        pitchtools.NamedPitchClass('ef'),
        pitchtools.NamedPitchClass('f'),])

    minor_second_ascending = pitchtools.NamedInterval('minor', 2)
    assert pitch_class_set_1.transpose(minor_second_ascending) == \
        pitch_class_set_2

    major_seventh_descending = pitchtools.NamedInterval('major', -7)
    assert pitch_class_set_1.transpose(major_seventh_descending) == \
        pitch_class_set_2

    minor_second_descending = pitchtools.NamedInterval('minor', -2)
    assert pitch_class_set_2.transpose(minor_second_descending) == \
        pitch_class_set_1

    major_seventh_ascending = pitchtools.NamedInterval('major', 7)
    assert pitch_class_set_2.transpose(major_seventh_ascending) == \
        pitch_class_set_1


def test_pitchtools_PitchClassSet_transpose_02():

    pitch_class_set = pitchtools.PitchClassSet([1, 2, 5])
    assert pitch_class_set.transpose(0) == pitchtools.PitchClassSet([1, 2, 5])
    assert pitch_class_set.transpose(1) == pitchtools.PitchClassSet([2, 3, 6])
    assert pitch_class_set.transpose(2) == pitchtools.PitchClassSet([3, 4, 7])
    assert pitch_class_set.transpose(3) == pitchtools.PitchClassSet([4, 5, 8])
    assert pitch_class_set.transpose(4) == pitchtools.PitchClassSet([5, 6, 9])
    assert pitch_class_set.transpose(5) == pitchtools.PitchClassSet([6, 7, 10])
    assert pitch_class_set.transpose(6) == pitchtools.PitchClassSet([7, 8, 11])
    assert pitch_class_set.transpose(7) == pitchtools.PitchClassSet([8, 9, 0])
    assert pitch_class_set.transpose(8) == pitchtools.PitchClassSet([9, 10, 1])
    assert pitch_class_set.transpose(9) == pitchtools.PitchClassSet([10, 11, 2])
    assert pitch_class_set.transpose(10) == pitchtools.PitchClassSet([11, 0, 3])
    assert pitch_class_set.transpose(11) == pitchtools.PitchClassSet([0, 1, 4])
