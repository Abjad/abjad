# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_make_spacer_skip_measures_01():
    r'''Make list of skip-populated measures.
    '''

    divisions = [(1, 8), (5, 16), (5, 16), (1, 4)]
    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = Staff(measures)
    scoretools.set_always_format_time_signature_of_measures_in_expr(staff)

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
