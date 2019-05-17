import abjad
import pytest


def test_Context___setattr___01():
    """
    Slots constrain context attributes.
    """

    context = abjad.Context([])

    with pytest.raises(AttributeError):
        context.foo = "bar"
