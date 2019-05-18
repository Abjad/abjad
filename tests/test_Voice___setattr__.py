import abjad
import pytest


def test_Voice___setattr___01():
    """
    Slots constrain voice attributes.
    """

    voice = abjad.Voice([])

    with pytest.raises(AttributeError):
        voice.foo = "bar"
