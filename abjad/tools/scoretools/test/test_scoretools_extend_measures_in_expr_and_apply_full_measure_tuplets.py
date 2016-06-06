# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_extend_measures_in_expr_and_apply_full_measure_tuplets_01():

    staff = Staff([Measure((2, 8), "c'8 d'8"), Measure((3, 8), "e'8 f'8 g'8")])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            e'8
            f'8
            g'8
        }
    }
    '''
    supplement = [Rest((1, 16))]
    result = scoretools.extend_measures_in_expr_and_apply_full_measure_tuplets(staff, supplement)

    r'''
    \new Staff {
        {
            \time 2/8
            \times 4/5 {
                c'8
                d'8
                r16
            }
        }
        {
            \time 3/8
            \tweak text #tuplet-number::calc-fraction-text
            \times 6/7 {
                e'8
                f'8
                g'8
                r16
            }
        }
    }
    '''

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                \times 4/5 {
                    c'8
                    d'8
                    r16
                }
            }
            {
                \time 3/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7 {
                    e'8
                    f'8
                    g'8
                    r16
                }
            }
        }
        '''
        )
