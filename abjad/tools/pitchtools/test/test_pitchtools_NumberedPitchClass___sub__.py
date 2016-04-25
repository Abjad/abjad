# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitchClass___sub___01():
    r'''Subtracting one pitch-class from another.
    '''

    pitch_class_1 = pitchtools.NumberedPitchClass(6)
    pitch_class_2 = pitchtools.NumberedPitchClass(7)

    assert pitch_class_1 - pitch_class_2 == \
        pitchtools.NumberedInversionEquivalentIntervalClass(1)
    assert pitch_class_2 - pitch_class_1 == \
        pitchtools.NumberedInversionEquivalentIntervalClass(1)


def test_pitchtools_NumberedPitchClass___sub___02():
    r'''Subtracting an interval-class from a pitch-class.
    '''

    pitch_class = pitchtools.NumberedPitchClass(0)
    interval_class = pitchtools.NumberedInversionEquivalentIntervalClass(2)

    assert pitch_class - interval_class == pitchtools.NumberedPitchClass(10)
    assert pytest.raises(TypeError, 'interval_class - pitch_class')
