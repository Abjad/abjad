from abjad import *

def test_tietools_get_tie_chains_in_expr_01():
    '''returns an empty list on a list of untied leaves.'''

    t = notetools.make_repeated_notes(4)
    chains = tietools.get_tie_chains_in_expr(t)

    assert chains == []


def test_tietools_get_tie_chains_in_expr_02():
    '''returns an empty list on a list of untied containers.'''

    t = Voice(notetools.make_repeated_notes(4))
    chains = tietools.get_tie_chains_in_expr([t])

    assert chains == []


def test_tietools_get_tie_chains_in_expr_03():
    '''returns an list of leaves on a list of tied leaves.'''

    t = notetools.make_repeated_notes(4)
    tietools.TieSpanner(t[0:2])
    chains = tietools.get_tie_chains_in_expr(t)

    assert chains == [tuple(t[0:2])]


def test_tietools_get_tie_chains_in_expr_04():
    '''returns an list of leaves on a list of tied containers.'''

    t = Voice(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t)
    chains = tietools.get_tie_chains_in_expr([t])

    assert chains == [tuple(t.leaves)]


def test_tietools_get_tie_chains_in_expr_05():
    '''returns an list of two elements if two Tie spanners are found.'''

    t = Voice("c'8 d'8 e'8 f'8")
    tietools.TieSpanner(t[0:2])
    tietools.TieSpanner(t[2:])
    chains = tietools.get_tie_chains_in_expr(t.leaves)

    assert chains == [tuple(t[0:2]), tuple(t[2:])]


def test_tietools_get_tie_chains_in_expr_06():
    '''returns an empty list if the given list of components is not
    tie-spanned, while its decendents are.'''

    t = Voice("c'8 d'8 e'8 f'8")
    tietools.TieSpanner(t[0:2])
    tietools.TieSpanner(t[2:])
    chains = tietools.get_tie_chains_in_expr([t])

    assert chains == []


def test_tietools_get_tie_chains_in_expr_07():
    '''returns an list those leaves that intersect a Tie spanner and the
    components given.'''

    t = Voice("c'8 d'8 e'8 f'8")
    tietools.TieSpanner(t.leaves)
    chains = tietools.get_tie_chains_in_expr(t.leaves[1:3])

    assert chains == [tuple(t.leaves[1:3])]


def test_tietools_get_tie_chains_in_expr_08():
    '''get_tie_chains() works across containers.'''

    t = Voice(Container("c'8 d'8 e'8 f'8") * 3)
    tietools.TieSpanner(t[0:2])
    chains = tietools.get_tie_chains_in_expr(t[:])

    assert chains == [tuple(t.leaves[0:8])]
