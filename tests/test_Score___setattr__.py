import pytest

import abjad


def test_Score___setattr___01():
    """
    Slots constrain score attributes.
    """

    score = abjad.Score([])

    with pytest.raises(AttributeError):
        score.foo = "bar"
