# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_TimeSignature_suppress_01():
    r'''Suppress time signature with power-of-two denominator at format-time.
    '''

    measure = Measure((7, 8), "c'8 d'8 e'8 f'8 g'8 a'8 b'8")
    measure.time_signature.suppress = True

    assert format(measure) == stringtools.normalize(
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


def test_indicatortools_TimeSignature_suppress_02():
    r'''Suppressing time signature without power-of-two denominator
    raises exception.
    '''

    measure = Measure((8, 9), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    measure.time_signature.suppress = True

    assert pytest.raises(Exception, 'format(measure)')
