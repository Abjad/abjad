# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_marktools_TimeSignatureMark_suppress_01():
    r'''Suppress time signature with power-of-two denominator at format-time.
    '''

    measure = Measure((7, 8), "c'8 d'8 e'8 f'8 g'8 a'8 b'8")
    measure.time_signature.suppress = True

    assert testtools.compare(
        measure,
        r'''
        {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
        }
        '''
        )


def test_marktools_TimeSignatureMark_suppress_02():
    r'''Suppressing time signature without power-of-two denominator 
    raises exception.
    '''

    measure = Measure((8, 9), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    measure.time_signature.suppress = True

    assert py.test.raises(Exception, 'format(measure)')
