from abjad import *


def test_StaffChangeMark___repr___01():
    '''Staff change mark returns nonempty string repr.
    '''

    staff = Staff([])
    staff.name = 'Flute Staff'
    repr = contexttools.StaffChangeMark(staff).__repr__()

    assert isinstance(repr, str) and 0 < len(repr)
