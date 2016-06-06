# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Score_add_final_bar_line_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    score = Score([staff])
    score.add_final_bar_line()

    r'''
    \new Score <<
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }
    >>
    '''

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                \bar "|."
            }
        >>
        '''
        )
