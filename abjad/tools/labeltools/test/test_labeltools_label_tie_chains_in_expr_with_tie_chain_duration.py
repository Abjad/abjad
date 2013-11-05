# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_tie_chains_in_expr_with_tie_chain_duration_01():

    staff = Staff(scoretools.make_repeated_notes(4))
    scoretools.FixedDurationTuplet(Duration(2, 8), staff[:3])
    tie = spannertools.TieSpanner()
    attach(tie, staff.select_leaves()[:2])
    tie = spannertools.TieSpanner()
    attach(tie, staff.select_leaves()[2:])
    labeltools.label_tie_chains_in_expr_with_tie_chain_duration(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'8 ~
                    _ \markup {
                        \small
                            1/6
                        }
                c'8
                c'8 ~
                    _ \markup {
                        \small
                            5/24
                        }
            }
            c'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
