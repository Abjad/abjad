# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_TieChain_leaves_group_by_immediate_parents_01():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves())

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

    tie_chain = inspect(staff.select_leaves()[0]).get_tie_chain()
    groups = tie_chain.leaves_grouped_by_immediate_parents

    assert len(groups) == 2
    assert groups[0] == list(staff.select_leaves()[:2])
    assert groups[1] == list(staff.select_leaves()[2:])


def test_selectiontools_TieChain_leaves_group_by_immediate_parents_02():

    staff = Staff("c'8 ~ c'8 ~ c'8 ~ c'8")
    tie_chain = inspect(staff.select_leaves()[0]).get_tie_chain()
    groups = tie_chain.leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == list(staff.select_leaves())


def test_selectiontools_TieChain_leaves_group_by_immediate_parents_03():

    note = Note("c'4")
    tie_chain = inspect(note).get_tie_chain()
    groups = tie_chain.leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == [note]
