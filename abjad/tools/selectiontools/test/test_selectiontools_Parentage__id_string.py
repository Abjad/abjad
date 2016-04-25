# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage__id_string_01():
    r'''Returns component name if it exists. Otherwise Python ID.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    parentage = inspect_(staff).get_parentage()
    assert parentage._id_string(staff).startswith('Staff-')


def test_selectiontools_Parentage__id_string_02():
    r'''Returns component name if it exists. Otherwise Python ID.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    parentage = inspect_(staff).get_parentage()
    staff.name = 'foo'
    assert parentage._id_string(staff) == "Staff-'foo'"
