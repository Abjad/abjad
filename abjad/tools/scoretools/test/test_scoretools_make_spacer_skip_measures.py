# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_make_spacer_skip_measures_01():
    r'''Make list of skip-populated measures.
    '''

    staff = Staff(scoretools.make_spacer_skip_measures([(1, 8), (5, 16), (5, 16), (1, 4)]))
    scoretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 1/8
            s1 * 1/8
        }
        {
            \time 5/16
            s1 * 5/16
        }
        {
            \time 5/16
            s1 * 5/16
        }
        {
            \time 1/4
            s1 * 1/4
        }
    }
    '''

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/8
                s1 * 1/8
            }
            {
                \time 5/16
                s1 * 5/16
            }
            {
                \time 5/16
                s1 * 5/16
            }
            {
                \time 1/4
                s1 * 1/4
            }
        }
        '''
        )
