import abjad
import pytest


def test_scoretools_Score___setattr___01():
    """
    Slots constrain score attributes.
    """

    score = abjad.Score([])

    assert pytest.raises(AttributeError, "score.foo = 'bar'")
