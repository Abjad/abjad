from abjad import *
import py.test


def test_Rest___setattr___01():
    '''Slots constrain rest attributes.
    '''

    rest = Rest((1, 4))

    assert py.test.raises(AttributeError, "rest.foo = 'bar'")
