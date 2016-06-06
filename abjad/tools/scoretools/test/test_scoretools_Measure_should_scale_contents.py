# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_should_scale_contents_01():

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8 f'8 g'8")
    measure = Measure((5, 12), [tuplet], implicit_scaling=False)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/12
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        }
        '''
        )
