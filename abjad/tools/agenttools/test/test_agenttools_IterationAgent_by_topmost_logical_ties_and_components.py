# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_topmost_logical_ties_and_components_01():
    r'''Iterates toplevel contents with logical ties in place of leaves.
    '''

    staff = Staff(r"c'8 ~ c'32 g'8 ~ g'32 a'8 ~ a'32 b'8 ~ b'32")
    tuplet = scoretools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    staff.insert(4, tuplet)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 ~
            c'32
            g'8 ~
            g'32
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            a'8 ~
            a'32
            b'8 ~
            b'32
        }
        '''
        )

    contents = iterate(staff).by_topmost_logical_ties_and_components()
    contents = list(contents)

    assert contents[0] == inspect_(staff[0]).get_logical_tie()
    assert contents[1] == inspect_(staff[2]).get_logical_tie()
    assert contents[2] is staff[4]
    assert contents[3] == inspect_(staff[5]).get_logical_tie()
    assert contents[4] == inspect_(staff[7]).get_logical_tie()
