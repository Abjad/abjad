# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval_numbered_interval_class_01():

    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(2)).number  == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(14)).number == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(26)).number == 2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(38)).number == 2


def test_pitchtools_NumberedInterval_numbered_interval_class_02():

    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-2)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-14)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-26)).number == -2
    assert pitchtools.NumberedIntervalClass(
        pitchtools.NumberedInterval(-38)).number == -2
