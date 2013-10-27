# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_measuretools_Measure_append_01():
    r'''Time signature does not automatically adjust.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.append('r')

    assert measure.is_overfull
    assert py.test.raises(Exception, 'f(measure)')


def test_measuretools_Measure_append_02():
    r'''Time signature adjusts automatically.
    '''

    measure = Measure((3, 4), "c' d' e'")
    measure.automatically_adjust_time_signature = True
    measure.append('r')

    assert not measure.is_misfilled
    assert testtools.compare(
        measure,
        r'''
        {
            \time 4/4
            c'4
            d'4
            e'4
            r4
        }
        '''
        )
