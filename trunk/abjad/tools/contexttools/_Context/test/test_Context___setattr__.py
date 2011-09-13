from abjad import *
from abjad.tools.contexttools._Context import _Context
import py.test


def test_Context___setattr___01():
    '''Slots constrain context attributes.
    '''

    context = _Context([])

    assert py.test.raises(AttributeError, "context.foo = 'bar'")
