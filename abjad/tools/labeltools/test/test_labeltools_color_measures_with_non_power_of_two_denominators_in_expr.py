# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_measures_with_non_power_of_two_denominators_in_expr_01():

    staff = Staff(2 * Measure((2, 8), "c'8 d'8"))
    scoretools.scale_measure_denominator_and_adjust_measure_contents(
        staff[1], 3)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8.
                    d'8.
                }
            }
        }
        '''
        )

    labeltools.color_measures_with_non_power_of_two_denominators_in_expr(
        staff, 'red')


    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \override Beam #'color = #red
                \override Dots #'color = #red
                \override NoteHead #'color = #red
                \override Staff.TimeSignature #'color = #red
                \override Stem #'color = #red
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8.
                    d'8.
                }
                \revert Beam #'color
                \revert Dots #'color
                \revert NoteHead #'color
                \revert Staff.TimeSignature #'color
                \revert Stem #'color
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
