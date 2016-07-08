# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie_leaves_group_by_immediate_parents_01():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    leaves = select(staff).by_leaf()
    tie = spannertools.Tie()
    attach(tie, leaves)

    r'''
    \new Staff {
            \time 2/8
            c'8 ~
            c'8 ~
            \time 2/8
            c'8 ~
            c'8
    }
    '''

    logical_tie = inspect_(leaves[0]).get_logical_tie()
    groups = logical_tie.leaves_grouped_by_immediate_parents

    assert len(groups) == 2
    assert groups[0] == leaves[:2]
    assert groups[1] == leaves[2:]


def test_selectiontools_LogicalTie_leaves_group_by_immediate_parents_02():

    staff = Staff("c'8 ~ c'8 ~ c'8 ~ c'8")
    logical_tie = inspect_(staff[0]).get_logical_tie()
    groups = logical_tie.leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == list(staff[:])


def test_selectiontools_LogicalTie_leaves_group_by_immediate_parents_03():

    note = Note("c'4")
    logical_tie = inspect_(note).get_logical_tie()
    groups = logical_tie.leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == [note]
