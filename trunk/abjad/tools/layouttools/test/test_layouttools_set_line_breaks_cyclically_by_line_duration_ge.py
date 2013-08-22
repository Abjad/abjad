# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import layouttools
from abjad.tools.leaftools.Leaf import Leaf


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_01():
    r'''Iterate classes in expr and accumulate prolated duration.
    Add line break after every total le line duration.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(staff, Duration(4, 8))
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
            \break
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
            \break
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
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
                \break
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
                \break
            }
        }
        '''
        )


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_02():
    r'''Iterate classes in expr and accumulate prolated duration.
    Add line break after every total le line duration.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(
        staff, Duration(1, 8), line_break_class=Leaf)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            \break
            d'8
            \break
        }
        {
            \time 2/8
            e'8
            \break
            f'8
            \break
        }
        {
            \time 2/8
            g'8
            \break
            a'8
            \break
        }
        {
            \time 2/8
            b'8
            \break
            c''8
            \break
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                \break
                d'8
                \break
            }
            {
                \time 2/8
                e'8
                \break
                f'8
                \break
            }
            {
                \time 2/8
                g'8
                \break
                a'8
                \break
            }
            {
                \time 2/8
                b'8
                \break
                c''8
                \break
            }
        }
        '''
        )
