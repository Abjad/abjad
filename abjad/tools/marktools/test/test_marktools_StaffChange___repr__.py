# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_StaffChange___repr___01():
    r'''Staff change returns nonempty string repr.
    '''

    staff = Staff([])
    staff.name = 'Flute Staff'
    repr = marktools.StaffChange(staff).__repr__()

    assert isinstance(repr, str) and 0 < len(repr)
