# -*- encoding: utf-8 -*-
from abjad import *


def test_TieChain_preprolated_duration_01():

    staff = Staff("c' ~ c'16")

    assert more(staff[0]).select_tie_chain()._preprolated_duration == Duration(5, 16)


def test_TieChain_preprolated_duration_02():

    staff = Staff("c'")

    assert more(staff[0]).select_tie_chain()._preprolated_duration == Duration(1, 4)
