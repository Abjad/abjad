import abjad
import pytest


def test_Context___setattr___01():
    """
    Slots constrain context attributes.
    """

    context = abjad.Context([])

    assert pytest.raises(AttributeError, "context.foo = 'bar'")