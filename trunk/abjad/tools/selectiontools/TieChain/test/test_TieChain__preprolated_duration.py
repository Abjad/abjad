# -*- encoding: utf-8 -*-
from abjad import *


def test_TieChain__preprolated_duration_01():

    staff = Staff("c' ~ c'16")

    assert inspect(staff[0]).get_tie_chain()._preprolated_duration == Duration(5, 16)


def test_TieChain__preprolated_duration_02():

    staff = Staff("c'")

    assert inspect(staff[0]).get_tie_chain()._preprolated_duration == Duration(1, 4)
