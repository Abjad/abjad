# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_01():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    staff = abjad.Staff(2 * abjad.Measure((2, 8), "c'8 c'8"))
    leaves = abjad.select(staff).by_leaf()
    tie = abjad.Tie()
    abjad.attach(tie, leaves)

    logical_tie = abjad.inspect(leaves[1]).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert format(staff) == abjad.String.normalize(
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
    assert abjad.inspect(staff).is_well_formed()


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_02():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    tie = abjad.Tie()
    abjad.attach(tie, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        '''
        )

    logical_tie = abjad.inspect(staff[1]).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'2
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()
    assert len(result) == 1


def test_selectiontools_LogicalTie__fuse_leaves_by_immediate_parent_03():
    r'''Fuse leaves in logical tie with same immediate parent.
    '''

    note = abjad.Note("c'4")
    logical_tie = abjad.inspect(note).get_logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()
    assert len(result) == 1
    assert abjad.inspect(note).is_well_formed()
