from abjad import *
import py.test


def test_Staff___setattr___01():
    '''Slots constrain staff attributes.
    '''

    staff = Staff([])

    assert py.test.raises(AttributeError, "staff.foo = 'bar'")
