# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_Measure___setitem___01():

    measure = Measure((3, 4), "c' d' e'")
    measure[:2] = 'r8'

    assert measure.is_underfull
    assert py.test.raises(Exception, 'f(measure)')


def test_Measure___setitem___02():

    measure = Measure((3, 4), "c' d' e'")
    measure.automatically_adjust_time_signature = True
    measure[:2] = 'r8'

    assert not measure.is_underfull
    assert testtools.compare(
        measure,
        r'''
        {
            \time 3/8
            r8
            e'4
        }
        '''
        )
