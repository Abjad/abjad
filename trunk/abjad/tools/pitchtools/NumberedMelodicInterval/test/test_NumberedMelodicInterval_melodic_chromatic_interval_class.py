# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicInterval_melodic_chromatic_interval_class_01():

    assert pitchtools.NumberedMelodicInterval(2).melodic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedMelodicInterval(14).melodic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedMelodicInterval(26).melodic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedMelodicInterval(38).melodic_chromatic_interval_class.number == 2


def test_NumberedMelodicInterval_melodic_chromatic_interval_class_02():

    assert pitchtools.NumberedMelodicInterval(-2).melodic_chromatic_interval_class.number == -2
    assert pitchtools.NumberedMelodicInterval(-14).melodic_chromatic_interval_class.number == -2
    assert pitchtools.NumberedMelodicInterval(-26).melodic_chromatic_interval_class.number == -2
    assert pitchtools.NumberedMelodicInterval(-38).melodic_chromatic_interval_class.number == -2
