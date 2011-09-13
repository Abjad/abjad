from abjad import *


def test_tietools_is_tie_chain_01():
    assert tietools.is_tie_chain(())


def test_tietools_is_tie_chain_02():
    t = Note("c'4")
    assert tietools.is_tie_chain(tietools.get_tie_chain(t))


def test_tietools_is_tie_chain_03():
    t = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[:2])
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[0]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[1]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[2]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[3]))


def test_tietools_is_tie_chain_04():
    t = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[:])
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[0]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[1]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[2]))
    assert tietools.is_tie_chain(tietools.get_tie_chain(t[3]))
