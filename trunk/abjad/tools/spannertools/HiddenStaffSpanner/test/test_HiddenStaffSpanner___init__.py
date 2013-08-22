# -*- encoding: utf-8 -*-
from abjad import *


def test_HiddenStaffSpanner___init___01():
    r'''Init empty hidden staff spanner.
    '''

    spanner = spannertools.HiddenStaffSpanner()
    assert isinstance(spanner, spannertools.HiddenStaffSpanner)


def test_HiddenStaffSpanner___init___02():
    r'''Hide staff around one measure.
    '''

    staff = Staff(Measure((2, 8), "c'8 d'8") * 3)
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

    spannertools.HiddenStaffSpanner(staff[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            \stopStaff
            e'8
            f'8
            \startStaff
        }
        {
            \time 2/8
            g'8
            a'8
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
                \stopStaff
                e'8
                f'8
                \startStaff
            }
            {
                \time 2/8
                g'8
                a'8
            }
        }
        '''
        )


def test_HiddenStaffSpanner___init___03():
    r'''Hide staff around one leaf.
    '''

    note = Note(0, (1, 8))
    spannertools.HiddenStaffSpanner(note)

    r'''
    \stopStaff
    c'8
    \startStaff
    '''

    assert inspect(note).is_well_formed()
    assert testtools.compare(
        note,
        r'''
        \stopStaff
        c'8
        \startStaff
        '''
        )
