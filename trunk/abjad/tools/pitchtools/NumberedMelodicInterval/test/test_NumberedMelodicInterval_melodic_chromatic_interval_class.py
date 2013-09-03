# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicInterval_melodic_chromatic_interval_class_01():

    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(2)).number  == 2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(14)).number == 2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(26)).number == 2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(38)).number == 2


def test_NumberedMelodicInterval_melodic_chromatic_interval_class_02():

    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(-2)).number == -2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(-14)).number == -2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(-26)).number == -2
    assert pitchtools.NumberedMelodicIntervalClass(
        pitchtools.NumberedMelodicInterval(-38)).number == -2
