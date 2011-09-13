from abjad import *


def test_tietools_get_preprolated_tie_chain_duration_01():
    '''Return sum of preprolated durations of leaves in tie chain.'''

    notes = notetools.make_notes(0, [(5, 16)])
    assert tietools.get_preprolated_tie_chain_duration(tietools.get_tie_chain(notes[0])) == \
        Duration(5, 16)


def test_tietools_get_preprolated_tie_chain_duration_02():
    '''Works on trivial tie chains.'''

    t = Note("c'4")
    assert tietools.get_preprolated_tie_chain_duration(tietools.get_tie_chain(t)) == Duration(1, 4)
