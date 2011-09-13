from abjad import *
import py.test


def test_Mark___setattr___01():
    '''Slots constraint mark attributes.
    '''

    mark = marktools.Mark()

    assert py.test.raises(AttributeError, "mark.foo = 'bar'")
