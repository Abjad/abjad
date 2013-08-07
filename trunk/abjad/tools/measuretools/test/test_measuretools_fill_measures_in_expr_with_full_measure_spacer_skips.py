# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_01():
    r'''Populate non-power-of-two measure with time-scaled skip.
    '''

    measure = Measure((5, 18), [])
    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(measure)

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            s1 * 5/16
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                s1 * 5/16
            }
        }
        '''
        )


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_02():
    r'''Populate measures conditionally.

    Iteration control tests index of iteration.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
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
        {
            \time 2/8
            b'8
            c''8
        }
    }
    '''

    def iterctrl(measure, i):
        return i % 2 == 1

    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(
        staff, iterctrl)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            s1 * 1/4
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            s1 * 1/4
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                s1 * 1/4
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                s1 * 1/4
            }
        }
        '''
        )


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_03():
    r'''Populate measures conditionally.

    Iteration control tests measure length.
    '''

    t = Staff([
        Measure((2, 8), "c'8 d'8"),
        Measure((3, 8), "c'8 d'8 e'8"),
        Measure((4, 8), "c'8 d'8 e'8 f'8"),
        ])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
    }
    '''

    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(t, lambda m, i: 2 < len(m))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            s1 * 3/8
        }
        {
            \time 4/8
            s1 * 1/2
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/8
                s1 * 3/8
            }
            {
                \time 4/8
                s1 * 1/2
            }
        }
        '''
        )
