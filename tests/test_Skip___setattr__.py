import abjad
import pytest


def test_Skip___setattr___01():
    """
    Slots constrain skip attributes.
    """

    skip = abjad.Skip((1, 4))

    with pytest.raises(AttributeError):
        skip.foo = "bar"
