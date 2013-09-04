# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedInterval_melodic_chromatic_interval_class_01():

    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(2)).number  == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(14)).number == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(26)).number == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(38)).number == 2


def test_NumberedInterval_melodic_chromatic_interval_class_02():

    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-2)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-14)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-26)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-38)).number == -2
