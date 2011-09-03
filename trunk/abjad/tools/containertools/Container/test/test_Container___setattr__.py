from abjad import *
import py.test


def test_Container___setattr___01():
    '''Slots constrain container attributes.
    '''

    container = Container([])

    assert py.test.raises(AttributeError, "container.foo = 'bar'")
