import abjad
import pytest


def test_LilyPondGrobNameManager___getattr___01():
    """
    Getting unknown grob name raises exception.
    """

    note = abjad.Note("c'8")
    with pytest.raises(Exception):
        abjad.override(note).foo
