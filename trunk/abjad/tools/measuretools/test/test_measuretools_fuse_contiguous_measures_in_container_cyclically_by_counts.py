# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_fuse_contiguous_measures_in_container_cyclically_by_counts_01():
    r'''Docs.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 5)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

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
        {
            \time 2/8
            d''8
            e''8
        }
    }
    '''

    part_counts = (2, 1)
    measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(staff, part_counts)

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 4/8
                c'8
                d'8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 4/8
                b'8
                c''8
                d''8
                e''8
            }
        }
        '''
        )


def test_measuretools_fuse_contiguous_measures_in_container_cyclically_by_counts_02():
    r'''Docs.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 5)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

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
        {
            \time 2/8
            d''8
            e''8
        }
    }
    '''

    part_counts = (3, )
    measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(
        staff, part_counts)

    r'''
    \new Staff {
        {
            \time 6/8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 6/8
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
            }
            {
                \time 4/8
                b'8
                c''8
                d''8
                e''8
            }
        }
        '''
        )
