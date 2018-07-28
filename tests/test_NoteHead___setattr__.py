import abjad
import pytest


def test_NoteHead___setattr___01():
    """
    Slots constrain note-head attributes.
    """

    note_head = abjad.NoteHead("cs''")

    assert pytest.raises(AttributeError, "note_head.foo = 'bar'")
