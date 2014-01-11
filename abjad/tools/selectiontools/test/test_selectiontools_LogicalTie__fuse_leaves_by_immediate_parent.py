# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_01():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    staff = Staff(2 * Measure((2, 8), "c'8 c'8"))
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves())

    logical_tie = inspect(staff.select_leaves()[1]).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                c'4
            }
        }
        '''
        )

    assert len(result) == 2
    assert inspect(staff).is_well_formed()


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_02():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    tie = spannertools.Tie()
    attach(tie, staff.select_leaves())

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        '''
        )

    logical_tie = inspect(staff.select_leaves()[1]).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'2
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 1


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_03():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    note = Note("c'4")
    logical_tie = inspect(note).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()
    assert len(result) == 1
    assert inspect(note).is_well_formed()
