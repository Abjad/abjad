import abjad
import pytest


def test_Note___setattr___01():
    """
    Slots constrain note attributes.
    """

    note = abjad.Note("c'4")

    with pytest.raises(AttributeError):
        note.foo = 'bar'
