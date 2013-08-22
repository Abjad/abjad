# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_comment_measures_in_container_with_measure_numbers_01():
    r'''Label measure numbers with comments before and after each measure.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)
    measuretools.comment_measures_in_container_with_measure_numbers(staff)

    r'''
    \new Staff {
        % start measure 1
        {
            \time 2/8
            c'8
            d'8
        }
        % stop measure 1
        % start measure 2
        {
            \time 2/8
            e'8
            f'8
        }
        % stop measure 2
        % start measure 3
        {
            \time 2/8
            g'8
            a'8
        }
        % stop measure 3
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            % start measure 1
            {
                \time 2/8
                c'8
                d'8
            }
            % stop measure 1
            % start measure 2
            {
                \time 2/8
                e'8
                f'8
            }
            % stop measure 2
            % start measure 3
            {
                \time 2/8
                g'8
                a'8
            }
            % stop measure 3
        }
        '''
        )


def test_measuretools_comment_measures_in_container_with_measure_numbers_02():
    r'''Works on measures, too, in addition to contexts.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)
    measuretools.comment_measures_in_container_with_measure_numbers(staff[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        % start measure 2
        {
            \time 2/8
            e'8
            f'8
        }
        % stop measure 2
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
            % start measure 2
            {
                \time 2/8
                e'8
                f'8
            }
            % stop measure 2
            {
                \time 2/8
                g'8
                a'8
            }
        }
        '''
        )
