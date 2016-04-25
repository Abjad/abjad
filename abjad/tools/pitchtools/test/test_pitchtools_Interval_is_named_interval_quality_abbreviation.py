# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Interval_is_named_interval_quality_abbreviation_01():

    assert pitchtools.Interval.is_named_interval_quality_abbreviation('M')
    assert pitchtools.Interval.is_named_interval_quality_abbreviation('m')
    assert pitchtools.Interval.is_named_interval_quality_abbreviation('P')
    assert pitchtools.Interval.is_named_interval_quality_abbreviation('aug')
    assert pitchtools.Interval.is_named_interval_quality_abbreviation('dim')


def test_pitchtools_Interval_is_named_interval_quality_abbreviation_02():

    assert not pitchtools.Interval.is_named_interval_quality_abbreviation('x')
    assert not pitchtools.Interval.is_named_interval_quality_abbreviation(17)
