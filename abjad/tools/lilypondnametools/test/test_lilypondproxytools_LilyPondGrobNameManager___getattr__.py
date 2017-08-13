import pytest
import abjad


def test_lilypondproxytools_LilyPondGrobNameManager___getattr___01():
    r'''Getting unknown grob name raises exception.
    '''

    note = abjad.Note("c'8")
    assert pytest.raises(Exception, 'override(note).foo')
