# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassVector___init___01():

    pcv = pitchtools.NumberedPitchClassVector([5, 6, 7, 8, 10, 11])
    assert pcv.chromatic_pitch_class_numbers == [5, 6, 7, 8, 10, 11]


def test_NumberedPitchClassVector___init___02():

    pcv = pitchtools.NumberedPitchClassVector([1.5, 5, 6, 7, 8, 10, 11])
    assert pcv.chromatic_pitch_class_numbers == [1.5, 5, 6, 7, 8, 10, 11]
