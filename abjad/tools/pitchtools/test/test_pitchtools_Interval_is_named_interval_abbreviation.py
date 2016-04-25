# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Interval_is_named_interval_abbreviation_01():

    assert pitchtools.Interval.is_named_interval_abbreviation('+M2')
    assert pitchtools.Interval.is_named_interval_abbreviation('+M9')
    assert pitchtools.Interval.is_named_interval_abbreviation('+M16')
    assert pitchtools.Interval.is_named_interval_abbreviation('-M2')
    assert pitchtools.Interval.is_named_interval_abbreviation('-M9')
    assert pitchtools.Interval.is_named_interval_abbreviation('-M16')


def test_pitchtools_Interval_is_named_interval_abbreviation_02():

    assert not pitchtools.Interval.is_named_interval_abbreviation(' M2')
