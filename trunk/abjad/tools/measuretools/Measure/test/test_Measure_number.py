# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_Measure_number_01():
    r'''Measures in staff number correctly starting from 1.
    '''

    time_signature_pairs = [(3, 16), (5, 16), (5, 16)]
    staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(time_signature_pairs))

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3


def test_Measure_number_02():
    r'''Orphan measures number correctly starting from 1.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    assert measure.measure_number == 1


def test_Measure_number_03():
    r'''Measure numbering works correctly after contents rotation.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3

    staff[:] = [staff[1], staff[2], staff[0]]
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
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
            c'8
            d'8
        }
    }
    '''

    assert staff[0].measure_number == 1
    assert staff[1].measure_number == 2
    assert staff[2].measure_number == 3

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
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
                c'8
                d'8
            }
        }
        '''
        )
