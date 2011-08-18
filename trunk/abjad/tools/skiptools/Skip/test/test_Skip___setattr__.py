from abjad import *
import py.test


def test_Skip___setattr___01():
    '''Slots constrain skip attributes.
    '''

    skip = skiptools.Skip((1, 4))

    assert py.test.raises(AttributeError, "skip.foo = 'bar'")
