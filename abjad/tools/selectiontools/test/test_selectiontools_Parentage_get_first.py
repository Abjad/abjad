# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Parentage_get_first_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        assert inspect_(leaf).get_parentage().get_first(Staff) is staff

    assert inspect_(staff).get_parentage(include_self=True).get_first(Staff) is staff
    assert inspect_(staff).get_parentage(include_self=False).get_first(Staff) is None
