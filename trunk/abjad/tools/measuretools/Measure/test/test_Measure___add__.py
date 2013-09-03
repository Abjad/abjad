# -*- encoding: utf-8 -*-
import py.test
from abjad import *


@py.test.skip()
def test_Measure___add___01():
    r'''Add outside-of-score measures.
    '''

    t1 = Measure((1, 8), "c'16 d'16")
    spannertools.BeamSpanner(t1[:])
    t2 = Measure((2, 16), "c'16 d'16")
    spannertools.SlurSpanner(t2[:])

    r'''
    {
        \time 1/8
        c'16 [
        d'16 ]
    }
    '''

    r'''
    {
        \time 2/16
        c'16 (
        d'16 )
    }
    '''

    new = t1 + t2

    r'''
    {
        \time 2/8
        c'16 [
        d'16 ]
        c'16 (
        d'16 )
    }
    '''

    assert new is not t1 and new is not t2
    assert len(t1) == 0
    assert len(t2) == 0
    assert inspect(new).is_well_formed()
    assert testtools.compare(
        new,
        r'''
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
        '''
        )


def test_Measure___add___02():
    r'''Add measures in score.
    '''

    t1 = Measure((1, 8), "c'16 d'16")
    spannertools.BeamSpanner(t1[:])
    t2 = Measure((2, 16), "c'16 d'16")
    spannertools.SlurSpanner(t2[:])
    staff = Staff([t1, t2])

    r'''
    \new Staff {
        {
            \time 1/8
            c'16 [
            d'16 ]
        }
        {
            \time 2/16
            c'16 (
            d'16 )
        }
    }
    '''

    new = t1 + t2

    r'''
    {
        \time 2/8
        c'16 [
        d'16 ]
        c'16 (
        d'16 )
    }
    '''

    assert new is not t1 and new is not t2
    assert len(t1) == 0
    assert len(t2) == 0
    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'16 [
                d'16 ]
                c'16 (
                d'16 )
            }
        }
        '''
        )
