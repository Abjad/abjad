# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_move_measure_prolation_to_full_measure_tuplet_01():
    r'''Move 3/12 prolation to full-measure tuplet.
    '''

    measure = Measure((2, 8), [])
    measure.append(r"\times 2/3 { \times 2/3 { c'16 d'16 e'16 } f'8 g'8 }")
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

    scoretools.move_measure_prolation_to_full_measure_tuplet(measure)

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

    assert inspect_(measure).is_well_formed()


def test_scoretools_move_measure_prolation_to_full_measure_tuplet_02():
    r'''Project time signature without power-of-two denominator
    onto measure with tied note values.
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

    scoretools.move_measure_prolation_to_full_measure_tuplet(measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/8
            \tweak text #tuplet-number::calc-fraction-text
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
        ), format(measure)

    assert inspect_(measure).is_well_formed()
