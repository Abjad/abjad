# -*- encoding: utf-8 -*-
from abjad import *


def test_pitcharraytools_PitchArray__get_composite_offset_difference_series_from_leavs_in_expr_01():

    staff_1 = Staff(r"\times 4/3 { c'8 d'8 e'8 }")
    staff_2 = Staff("f'8 g'8 a'8 b'8")
    score = Score([staff_1, staff_2])

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }
            }
            \new Staff {
                f'8
                g'8
                a'8
                b'8
            }
        >>
        '''
        )

    result = pitcharraytools.PitchArray._get_composite_offset_difference_series_from_leaves_in_expr(score)

    assert result == [
        Duration(1, 8), 
        Duration(1, 24), 
        Duration(1, 12), 
        Duration(1, 12), 
        Duration(1, 24), 
        Duration(1, 8),
        ]
