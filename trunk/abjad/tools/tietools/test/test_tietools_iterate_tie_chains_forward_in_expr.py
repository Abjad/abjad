from abjad import *


def test_tietools_iterate_tie_chains_forward_in_expr_01():
    '''Yield successive tie chains.'''

    t = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[:2])
    tietools.TieSpanner(t[2:])

    r'''
    \new Staff {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    chains = list(tietools.iterate_tie_chains_forward_in_expr(t))

    assert chains[0] == (t[0], t[1])
    assert chains[1] == (t[2], t[3])


def test_tietools_iterate_tie_chains_forward_in_expr_02():
    '''Yield successive tie chains.'''

    t = Staff(notetools.make_repeated_notes(4))

    r'''
    \new Staff {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    chains = list(tietools.iterate_tie_chains_forward_in_expr(t))

    assert chains[0] == (t[0], )
    assert chains[1] == (t[1], )
    assert chains[2] == (t[2], )
    assert chains[3] == (t[3], )
