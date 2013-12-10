# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_logical_ties_in_expr_with_written_logical_tie_duration_01():

    staff = Staff(scoretools.make_repeated_notes(4))
    scoretools.FixedDurationTuplet(Duration(2, 8), staff[:3])
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves()[:2])
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves()[2:])
    labeltools.label_logical_ties_in_expr_with_written_logical_tie_duration(
        staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'8 ~
                    _ \markup {
                        \small
                            1/4
                        }
                c'8
                c'8 ~
                    _ \markup {
                        \small
                            1/4
                        }
            }
            c'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
