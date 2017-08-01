# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Measure___setitem___01():

    measure = abjad.Measure((3, 4), "c' d' e'")
    measure[:2] = 'r8'

    assert measure.is_underfull
    assert pytest.raises(Exception, 'f(measure)')


def test_scoretools_Measure___setitem___02():

    measure = abjad.Measure((3, 4), "c' d' e'")
    measure.automatically_adjust_time_signature = True
    measure[:2] = 'r8'

    assert not measure.is_underfull
    assert format(measure) == abjad.String.normalize(
        r'''
        {
            \time 3/8
            r8
            e'4
        }
        '''
        )
