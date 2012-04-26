from abjad import *


def test_TieChain_leaves_group_by_immediate_parents_01():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    tietools.TieSpanner(staff.leaves)

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

    groups = tietools.get_tie_chain(staff.leaves[0]).leaves_grouped_by_immediate_parents

    assert len(groups) == 2
    assert groups[0] == list(staff.leaves[:2])
    assert groups[1] == list(staff.leaves[2:])


def test_TieChain_leaves_group_by_immediate_parents_02():

    staff = Staff("c'8 ~ c'8 ~ c'8 ~ c'8")
    groups = tietools.get_tie_chain(staff[0]).leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == list(staff.leaves)


def test_TieChain_leaves_group_by_immediate_parents_03():

    note = Note("c'4")
    groups = tietools.get_tie_chain(note).leaves_grouped_by_immediate_parents

    assert len(groups) == 1
    assert groups[0] == [note]
