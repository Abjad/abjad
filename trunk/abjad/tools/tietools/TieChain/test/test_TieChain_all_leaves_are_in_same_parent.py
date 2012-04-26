from abjad import *


def test_TieChain_all_leaves_are_in_same_parent_01():


    staff = notetools.make_repeated_notes(4)
    tietools.TieSpanner(staff[:])

    assert tietools.get_tie_chain(staff[0]).all_leaves_are_in_same_parent


def test_TieChain_all_leaves_are_in_same_parent_02():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    tietools.TieSpanner(staff.leaves[1:3])

    r'''
    \new Staff {
            \time 2/8
            c'8
            c'8 ~
            \time 2/8
            c'8
            c'8
    }
    '''

    assert tietools.get_tie_chain(staff.leaves[0]).all_leaves_are_in_same_parent
    assert not tietools.get_tie_chain(staff.leaves[1]).all_leaves_are_in_same_parent
    assert not tietools.get_tie_chain(staff.leaves[2]).all_leaves_are_in_same_parent
    assert tietools.get_tie_chain(staff.leaves[3]).all_leaves_are_in_same_parent


def test_TieChain_all_leaves_are_in_same_parent_03():

    staff = Staff(r"\times 2/3 { c'8 c'8 c'8 ~ } \times 2/3 { c'8 c'8 c'8 }")

    r'''
    \new Staff {
        \times 2/3 {
            c'8
            c'8
            c'8 ~
        }
        \times 2/3 {
            c'8
            c'8
            c'8
        }
    }
    '''

    assert tietools.get_tie_chain(staff.leaves[0]).all_leaves_are_in_same_parent
    assert tietools.get_tie_chain(staff.leaves[1]).all_leaves_are_in_same_parent
    assert not tietools.get_tie_chain(staff.leaves[2]).all_leaves_are_in_same_parent
    assert not tietools.get_tie_chain(staff.leaves[3]).all_leaves_are_in_same_parent
    assert tietools.get_tie_chain(staff.leaves[4]).all_leaves_are_in_same_parent
    assert tietools.get_tie_chain(staff.leaves[5]).all_leaves_are_in_same_parent
