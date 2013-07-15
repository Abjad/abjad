from abjad import *
import py.test


def test_VerticalMoment___setattr___01():
    '''Vertical moments are immutable.
    '''

    vertical_moment = Note('c4').select_vertical_moment()
    assert py.test.raises(AttributeError, "vertical_moment.foo = 'bar'")
