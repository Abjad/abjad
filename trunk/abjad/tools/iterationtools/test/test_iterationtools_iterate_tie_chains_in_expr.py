# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_tie_chains_in_expr_01():
    r'''Yield successive tie chains.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    tie = spannertools.TieSpanner()
    attach(tie, staff[:2])
    tie = spannertools.TieSpanner()
    attach(tie, staff[2:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ~
            c'8
            c'8 ~
            c'8
        }
        '''
        )

    chains = list(
        iterationtools.iterate_tie_chains_in_expr(staff, reverse=True))

    assert chains[0] == selectiontools.TieChain((staff[2], staff[3]))
    assert chains[1] == selectiontools.TieChain((staff[0], staff[1]))


def test_iterationtools_iterate_tie_chains_in_expr_02():
    r'''Yield successive tie chains.
    '''

    staff = Staff(notetools.make_repeated_notes(4))

    chains = list(
        iterationtools.iterate_tie_chains_in_expr(staff, reverse=True))

    assert chains[0] == selectiontools.TieChain(staff[3])
    assert chains[1] == selectiontools.TieChain(staff[2])
    assert chains[2] == selectiontools.TieChain(staff[1])
    assert chains[3] == selectiontools.TieChain(staff[0])


def test_iterationtools_iterate_tie_chains_in_expr_03():
    r'''Yield successive tie chains.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    tie = spannertools.TieSpanner()
    attach(tie, staff[:2])
    tie = spannertools.TieSpanner()
    attach(tie, staff[2:])

    chains = list(iterationtools.iterate_tie_chains_in_expr(staff))

    assert chains[0] == selectiontools.TieChain((staff[0], staff[1]))
    assert chains[1] == selectiontools.TieChain((staff[2], staff[3]))


def test_iterationtools_iterate_tie_chains_in_expr_04():
    r'''Yield successive tie chains.
    '''

    staff = Staff(notetools.make_repeated_notes(4))

    r'''
    \new Staff {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    chains = list(iterationtools.iterate_tie_chains_in_expr(staff))

    assert chains[0] == selectiontools.TieChain(staff[0])
    assert chains[1] == selectiontools.TieChain(staff[1])
    assert chains[2] == selectiontools.TieChain(staff[2])
    assert chains[3] == selectiontools.TieChain(staff[3])
