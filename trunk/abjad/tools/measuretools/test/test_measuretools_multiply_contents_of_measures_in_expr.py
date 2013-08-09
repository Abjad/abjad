# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_multiply_contents_of_measures_in_expr_01():
    r'''Multiply contents of measure 3 times.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.multiply_contents_of_measures_in_expr(measure, 3)

    r'''
    {
        \time 9/8
        c'8
        d'8
        e'8
        c'8
        d'8
        e'8
        c'8
        d'8
        e'8
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 9/8
            c'8
            d'8
            e'8
            c'8
            d'8
            e'8
            c'8
            d'8
            e'8
        }
        '''
        )


def test_measuretools_multiply_contents_of_measures_in_expr_02():
    r'''Multiply contents of each measure 3 times.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    measuretools.multiply_contents_of_measures_in_expr(staff, 2)

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            d'8
            c'8
            d'8
        }
        {
            \time 4/8
            e'8
            f'8
            e'8
            f'8
        }
        {
            \time 4/8
            g'8
            a'8
            g'8
            a'8
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 4/8
                c'8
                d'8
                c'8
                d'8
            }
            {
                \time 4/8
                e'8
                f'8
                e'8
                f'8
            }
            {
                \time 4/8
                g'8
                a'8
                g'8
                a'8
            }
        }
        '''
        )
