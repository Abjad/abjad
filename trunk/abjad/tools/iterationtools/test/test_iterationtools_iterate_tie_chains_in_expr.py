from abjad import *


def test_iterationtools_iterate_tie_chains_in_expr_01():
    r'''Yield successive tie chains.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(t[:2])
    spannertools.TieSpanner(t[2:])

    r'''
    \new Staff {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    chains = list(iterationtools.iterate_tie_chains_in_expr(t, reverse=True))

    assert chains[0] == leaftools.TieChain((t[2], t[3]))
    assert chains[1] == leaftools.TieChain((t[0], t[1]))


def test_iterationtools_iterate_tie_chains_in_expr_02():
    r'''Yield successive tie chains.
    '''

    t = Staff(notetools.make_repeated_notes(4))

    r'''
    \new Staff {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    chains = list(iterationtools.iterate_tie_chains_in_expr(t, reverse=True))

    assert chains[0] == leaftools.TieChain(t[3])
    assert chains[1] == leaftools.TieChain(t[2])
    assert chains[2] == leaftools.TieChain(t[1])
    assert chains[3] == leaftools.TieChain(t[0])


def test_iterationtools_iterate_tie_chains_in_expr_03():
    r'''Yield successive tie chains.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(t[:2])
    spannertools.TieSpanner(t[2:])

    r'''
    \new Staff {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    chains = list(iterationtools.iterate_tie_chains_in_expr(t))

    assert chains[0] == leaftools.TieChain((t[0], t[1]))
    assert chains[1] == leaftools.TieChain((t[2], t[3]))


def test_iterationtools_iterate_tie_chains_in_expr_04():
    r'''Yield successive tie chains.
    '''

    t = Staff(notetools.make_repeated_notes(4))

    r'''
    \new Staff {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    chains = list(iterationtools.iterate_tie_chains_in_expr(t))

    assert chains[0] == leaftools.TieChain(t[0])
    assert chains[1] == leaftools.TieChain(t[1])
    assert chains[2] == leaftools.TieChain(t[2])
    assert chains[3] == leaftools.TieChain(t[3])
