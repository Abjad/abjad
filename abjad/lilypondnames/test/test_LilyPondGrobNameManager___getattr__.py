import pytest
import abjad


def test_LilyPondGrobNameManager___getattr___01():
    """
    Getting unknown grob name raises exception.
    """

    note = abjad.Note("c'8")
    assert pytest.raises(Exception, 'override(note).foo')
