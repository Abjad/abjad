# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie__preprolated_duration_01():

    staff = Staff("c' ~ c'16")

    assert inspect_(staff[0]).get_logical_tie()._preprolated_duration == Duration(5, 16)


def test_selectiontools_LogicalTie__preprolated_duration_02():

    staff = Staff("c'")

    assert inspect_(staff[0]).get_logical_tie()._preprolated_duration == Duration(1, 4)
