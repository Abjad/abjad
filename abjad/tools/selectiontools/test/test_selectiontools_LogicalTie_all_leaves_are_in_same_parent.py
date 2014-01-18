# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie_all_leaves_are_in_same_parent_01():


    staff = scoretools.make_repeated_notes(4)
    tie = spannertools.Tie()
    attach(tie, staff[:])

    assert inspect_(staff[0]).get_logical_tie().all_leaves_are_in_same_parent


def test_selectiontools_LogicalTie_all_leaves_are_in_same_parent_02():

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves()[1:3])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                c'8 ~
            }
            {
                c'8
                c'8
            }
        }
        '''
        )

    assert inspect_(staff.select_leaves()[0]).get_logical_tie().all_leaves_are_in_same_parent
    assert not inspect_(staff.select_leaves()[1]).get_logical_tie().all_leaves_are_in_same_parent
    assert not inspect_(staff.select_leaves()[2]).get_logical_tie().all_leaves_are_in_same_parent
    assert inspect_(staff.select_leaves()[3]).get_logical_tie().all_leaves_are_in_same_parent


def test_selectiontools_LogicalTie_all_leaves_are_in_same_parent_03():

    staff = Staff(r"\times 2/3 { c'8 c'8 c'8 ~ } \times 2/3 { c'8 c'8 c'8 }")

    assert systemtools.TestManager.compare(
        staff,
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
        )

    assert inspect_(staff.select_leaves()[0]).get_logical_tie().all_leaves_are_in_same_parent
    assert inspect_(staff.select_leaves()[1]).get_logical_tie().all_leaves_are_in_same_parent
    assert not inspect_(staff.select_leaves()[2]).get_logical_tie().all_leaves_are_in_same_parent
    assert not inspect_(staff.select_leaves()[3]).get_logical_tie().all_leaves_are_in_same_parent
    assert inspect_(staff.select_leaves()[4]).get_logical_tie().all_leaves_are_in_same_parent
    assert inspect_(staff.select_leaves()[5]).get_logical_tie().all_leaves_are_in_same_parent
