from abjad import *


def test_TieChain_all_leaves_are_in_same_parent_01():


    staff = notetools.make_repeated_notes(4)
    tietools.TieSpanner(staff[:])

    assert staff[0].get_tie_chain().all_leaves_are_in_same_parent


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

    assert staff.leaves[0].get_tie_chain().all_leaves_are_in_same_parent
    assert not staff.leaves[1].get_tie_chain().all_leaves_are_in_same_parent
    assert not staff.leaves[2].get_tie_chain().all_leaves_are_in_same_parent
    assert staff.leaves[3].get_tie_chain().all_leaves_are_in_same_parent


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

    assert staff.leaves[0].get_tie_chain().all_leaves_are_in_same_parent
    assert staff.leaves[1].get_tie_chain().all_leaves_are_in_same_parent
    assert not staff.leaves[2].get_tie_chain().all_leaves_are_in_same_parent
    assert not staff.leaves[3].get_tie_chain().all_leaves_are_in_same_parent
    assert staff.leaves[4].get_tie_chain().all_leaves_are_in_same_parent
    assert staff.leaves[5].get_tie_chain().all_leaves_are_in_same_parent
