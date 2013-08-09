# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_01():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    spannertools.TieSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
      {
            \time 2/8
            c'8 ~
            c'8 ~
      }
      {
            \time 2/8
            c'8 ~
            c'8
      }
    }
    '''

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        staff.select_leaves()[1].select_tie_chain())

    r'''
    \new Staff {
      {
            \time 2/8
            c'4 ~
      }
      {
            \time 2/8
            c'4
      }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(result) == 2
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                \time 2/8
                c'4
            }
        }
        '''
        )


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_02():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(staff.select_leaves())

    r'''
    \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
    }
    '''

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        staff.select_leaves()[1].select_tie_chain())

    assert select(staff).is_well_formed()
    assert len(result) == 1
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'2
        }
        '''
        )


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_03():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    note = Note("c'4")
    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        note.select_tie_chain())
    assert len(result) == 1
    assert select(note).is_well_formed()
