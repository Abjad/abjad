import abjad
import pytest


def test_scoretools_Context___setattr___01():
    r'''Slots constrain context attributes.
    '''

    context = abjad.Context([])

    assert pytest.raises(AttributeError, "context.foo = 'bar'")
