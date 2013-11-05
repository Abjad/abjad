# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_StaffChangeMark___repr___01():
    r'''Staff change mark returns nonempty string repr.
    '''

    staff = Staff([])
    staff.name = 'Flute Staff'
    repr = marktools.StaffChangeMark(staff).__repr__()

    assert isinstance(repr, str) and 0 < len(repr)
