# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeSignatureMark_suppress_01():
    r'''Suppress time signature with power-of-two denominator at format-time.
    '''

    t = Measure((7, 8), "c'8 d'8 e'8 f'8 g'8 a'8 b'8")
    t.get_effective_context_mark(
        contexttools.TimeSignatureMark).suppress = True

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

    assert testtools.compare(
        t.lilypond_format,
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


def test_TimeSignatureMark_suppress_02():
    r'''Suppressing time signature without power-of-two denominator raises exception.
    '''

    t = Measure((8, 9), "c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    t.get_effective_context_mark(
        contexttools.TimeSignatureMark).suppress = True

    assert py.test.raises(Exception, 't.lilypond_format')
