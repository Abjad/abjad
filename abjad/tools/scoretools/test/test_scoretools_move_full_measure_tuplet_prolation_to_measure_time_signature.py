# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_01():
    r'''Move prolation of full-measure power-of-two tuplet to time signature.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    measure = Measure((2, 8), [tuplet])
    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(
        measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
            }
        }
        '''
        ), format(measure)

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_02():
    r'''Move prolation of full-measure non-power-of-two tuplet to
    time signature.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(3, 16), [])
    tuplet.extend("c'16 d'16 e'16 f'16 g'16")
    measure = Measure((3, 16), [tuplet])
    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(
        measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 15/80
            \scaleDurations #'(4 . 5) {
                c'32.
                d'32.
                e'32.
                f'32.
                g'32.
            }
        }
        '''
        ), format(measure)

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_03():
    r'''Subsume 7:6 tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(6, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
    measure = Measure((6, 8), [tuplet])
    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(
        measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 21/28
            \scaleDurations #'(4 . 7) {
                c'8.
                d'8.
                e'8.
                f'8.
                g'8.
                a'8.
                b'8.
            }
        }
        '''
        ), format(measure)

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_04():
    r'''Subsume tuplet in nonassignable measure.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(5, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8 a'8")
    measure = Measure((5, 8), [tuplet])
    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(
        measure)

    assert format(measure) == stringtools.normalize(
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
        ), format(measure)

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_05():
    r'''Subsume nested tuplet.
    '''

    measure = Measure((2, 8), [])
    measure.append(r"\times 2/3 { \times 2/3 { c'16 d'16 e'16 } f'8 g'8 }")

    assert format(measure) == stringtools.normalize(
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
        ), format(measure)

    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(
        measure)

    assert format(measure) == stringtools.normalize(
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
        ), format(measure)

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_full_measure_tuplet_prolation_to_measure_time_signature_06():
    r'''Submsume 6:5. Time signature should go from 5/16 to 15/48.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(5, 16), "c'8 d'8 e'8")
    measure = Measure((5, 16), [tuplet])

    r'''
    {
        \time 5/16
        \tweak text #tuplet-number::calc-fraction-text
        \times 5/6 {
            c'8
            d'8
            e'8
        }
    }
    '''

    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature(measure)

    r'''
    {
        \time 15/48
        \scaleDurations #'(2 . 3) {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
        }
    }
    '''

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 15/48
            \scaleDurations #'(2 . 3) {
                c'8 ~
                c'32
                d'8 ~
                d'32
                e'8 ~
                e'32
            }
        }
        '''
        ), format(measure)
