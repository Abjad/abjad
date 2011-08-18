from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_are_stepwise_ascending_notes_01():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    staff = Staff(notes)

    assert tonalitytools.are_stepwise_ascending_notes(staff.leaves)


def test_tonalitytools_are_stepwise_ascending_notes_02():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    notes.reverse()
    staff = Staff(notes)

    assert not tonalitytools.are_stepwise_ascending_notes(staff.leaves)
