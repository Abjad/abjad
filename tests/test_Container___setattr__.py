import abjad
import pytest


def test_Container___setattr___01():
    """
    Slots constrain container attributes.
    """

    container = abjad.Container([])

    with pytest.raises(AttributeError):
        container.foo = "bar"
