from abjad import *
from abjad.tools.contexttools.Context import Context
import py.test


def test_Context___setattr___01():
    '''Slots constrain context attributes.
    '''

    context = Context([])

    assert py.test.raises(AttributeError, "context.foo = 'bar'")
