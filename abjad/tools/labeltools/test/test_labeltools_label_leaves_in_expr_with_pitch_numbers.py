# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_pitch_numbers_01():
    r'''Works on notes, rests and chords.
    '''

    leaves = scoretools.make_leaves([None, 12, (13, 14, 15), None], [(1, 4)])
    staff = Staff(leaves)
    labeltools.label_leaves_in_expr_with_pitch_numbers(staff)

    r'''
    \new Staff {
        r4
        c''4
            _ \markup {
                \small
                    12
                }
        <cs'' d'' ef''>4
            _ \markup {
                \column
                    {
                        \small
                            15
                        \small
                            14
                        \small
                            13
                    }
                }
        r4
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            r4
            c''4
                _ \markup {
                    \small
                        12
                    }
            <cs'' d'' ef''>4
                _ \markup {
                    \column
                        {
                            \small
                                15
                            \small
                                14
                            \small
                                13
                        }
                    }
            r4
        }
        '''
        )
