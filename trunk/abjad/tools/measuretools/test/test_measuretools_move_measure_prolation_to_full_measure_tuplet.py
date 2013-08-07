# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_move_measure_prolation_to_full_measure_tuplet_01():
    r'''Project 3/12 time signature onto measure contents.
    '''

    inner = tuplettools.FixedDurationTuplet(Duration(2, 16),
        notetools.make_repeated_notes(3, Duration(1, 16)))
    notes = notetools.make_repeated_notes(2)
    outer = tuplettools.FixedDurationTuplet(Duration(2, 8), [inner] + notes)
    measure = Measure((2, 8), [outer])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(measure)
    measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature(measure)

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            \times 2/3 {
                c'16
                d'16
                e'16
            }
            f'8
            g'8
        }
    }
    '''

    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                \times 2/3 {
                    c'16
                    d'16
                    e'16
                }
                f'8
                g'8
            }
        }
        '''
        )


    measuretools.move_measure_prolation_to_full_measure_tuplet(measure)

    r'''
    {
        \time 2/8
        \times 2/3 {
            \times 2/3 {
                c'16
                d'16
                e'16
            }
            f'8
            g'8
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 2/8
            \times 2/3 {
                \times 2/3 {
                    c'16
                    d'16
                    e'16
                }
                f'8
                g'8
            }
        }
        '''
        )


def test_measuretools_move_measure_prolation_to_full_measure_tuplet_02():
    r'''Project time signature without power-of-two denominator
    onto measure with tied note values.
    '''

    t = Measure((5, 8), [tuplettools.FixedDurationTuplet(Duration(5, 8), "c'8 d'8 e'8 f'8 g'8 a'8")])
    measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature(t)

    r'''
    {
        \time 15/24
        \scaleDurations #'(2 . 3) {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
            g'8 ~
            g'32
            a'8 ~
            a'32
        }
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            \time 15/24
            \scaleDurations #'(2 . 3) {
                c'8 ~
                c'32
                d'8 ~
                d'32
                e'8 ~
                e'32
                f'8 ~
                f'32
                g'8 ~
                g'32
                a'8 ~
                a'32
            }
        }
        '''
        )

    measuretools.move_measure_prolation_to_full_measure_tuplet(t)

    r'''
    {
        \time 5/8
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 5/6 {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            \time 5/8
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 5/6 {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
            }
        }
        '''
        )
