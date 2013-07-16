from abjad import *


def test_TieChain_all_leaves_are_in_same_parent_01():


    staff = notetools.make_repeated_notes(4)
    spannertools.TieSpanner(staff[:])

    assert staff[0].select_tie_chain().all_leaves_are_in_same_parent


def test_TieChain_all_leaves_are_in_same_parent_02():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    spannertools.TieSpanner(staff.select_leaves()[1:3])

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

    assert staff.select_leaves()[0].select_tie_chain().all_leaves_are_in_same_parent
    assert not staff.select_leaves()[1].select_tie_chain().all_leaves_are_in_same_parent
    assert not staff.select_leaves()[2].select_tie_chain().all_leaves_are_in_same_parent
    assert staff.select_leaves()[3].select_tie_chain().all_leaves_are_in_same_parent


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

    assert staff.select_leaves()[0].select_tie_chain().all_leaves_are_in_same_parent
    assert staff.select_leaves()[1].select_tie_chain().all_leaves_are_in_same_parent
    assert not staff.select_leaves()[2].select_tie_chain().all_leaves_are_in_same_parent
    assert not staff.select_leaves()[3].select_tie_chain().all_leaves_are_in_same_parent
    assert staff.select_leaves()[4].select_tie_chain().all_leaves_are_in_same_parent
    assert staff.select_leaves()[5].select_tie_chain().all_leaves_are_in_same_parent
