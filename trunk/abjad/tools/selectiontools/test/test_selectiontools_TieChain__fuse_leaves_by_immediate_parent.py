# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_TieChain__fuse_leaves_by_immediate_parent_01():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    spannertools.TieSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    # comparison function breaks here for unknown reason
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

    tie_chain = inspect(staff.select_leaves()[1]).get_tie_chain()
    result = tie_chain._fuse_leaves_by_immediate_parent()

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

    assert len(result) == 2
    assert inspect(staff).is_well_formed()


def test_selectiontools_TieChain__fuse_leaves_by_immediate_parent_02():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(staff.select_leaves())

    # comparison function breaks here for unknown reason
    r'''
    \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
    }
    '''

    tie_chain = inspect(staff.select_leaves()[1]).get_tie_chain()
    result = tie_chain._fuse_leaves_by_immediate_parent()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'2
        }
        '''
        )

    assert inspect(staff).is_well_formed()
    assert len(result) == 1


def test_selectiontools_TieChain__fuse_leaves_by_immediate_parent_03():
    r'''Fuse leaves in tie chain with same immediate parent.
    '''

    note = Note("c'4")
    tie_chain = inspect(note).get_tie_chain()
    result = tie_chain._fuse_leaves_by_immediate_parent()
    assert len(result) == 1
    assert inspect(note).is_well_formed()
