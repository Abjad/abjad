# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_StaffChange_staff_01():
    r'''Staff of staff change is read / write.
    '''

    rh_staff = Staff("c'8 d'8 e'8 f'8")
    rh_staff.name = 'RHStaff'
    staff_change = marktools.StaffChange(rh_staff)
    assert staff_change.staff is rh_staff

    lh_staff = Staff("s2")
    lh_staff.name = 'LHStaff'
    staff_change.staff = lh_staff
    assert staff_change.staff is lh_staff
