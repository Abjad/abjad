from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_is_neighbor_note_01():

    notes = notetools.make_notes([0, 2, 4, 2, 0], [(1, 4)])
    t = Staff(notes)

    assert not tonalitytools.is_neighbor_note(t[0])
    assert not tonalitytools.is_neighbor_note(t[1])
    assert tonalitytools.is_neighbor_note(t[2])
    assert not tonalitytools.is_neighbor_note(t[3])
    assert not tonalitytools.is_neighbor_note(t[4])
