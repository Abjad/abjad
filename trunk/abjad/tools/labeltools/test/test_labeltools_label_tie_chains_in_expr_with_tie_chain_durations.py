# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_tie_chains_in_expr_with_tie_chain_durations_01():

    staff = Staff(notetools.make_repeated_notes(4))
    tuplettools.FixedDurationTuplet(Duration(2, 8), staff[:3])
    spannertools.TieSpanner(staff.select_leaves()[:2])
    spannertools.TieSpanner(staff.select_leaves()[2:])
    labeltools.label_tie_chains_in_expr_with_tie_chain_durations(staff)

    r'''
    \new Staff {
        \times 2/3 {
            c'8 ~
                _ \markup {
                    \column {
                        \small
                            1/4
                        \small
                            1/6
                        }
                    }
            c'8
            c'8 ~
                _ \markup {
                    \column {
                        \small
                            1/4
                        \small
                            5/24
                        }
                    }
        }
        c'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'8 ~
                    _ \markup {
                        \column
                            {
                                \small
                                    1/4
                                \small
                                    1/6
                            }
                        }
                c'8
                c'8 ~
                    _ \markup {
                        \column
                            {
                                \small
                                    1/4
                                \small
                                    5/24
                            }
                        }
            }
            c'8
        }
        '''
        )
