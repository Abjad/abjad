from abjad import *


def test_tietools_get_leaves_in_tie_chain_01():
    '''Leaves from nontrivial tie chain.'''

    notes = notetools.make_notes(0, [(5, 32)])
    assert tietools.get_leaves_in_tie_chain(tietools.get_tie_chain(notes[0])) == tuple(notes)


def test_tietools_get_leaves_in_tie_chain_02():
    '''Leaves from trivial tie chain.'''

    t = Note("c'4")
    assert tietools.get_leaves_in_tie_chain(tietools.get_tie_chain(t)) == (t, )
