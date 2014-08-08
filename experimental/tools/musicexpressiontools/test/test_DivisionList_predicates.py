# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.DivisionList import DivisionList


def test_DivisionList_predicates_01():

    division_list = DivisionList([(4, 8), (4, 8), (3, 8)])

    assert division_list.is_left_closed
    assert not division_list.is_left_open

    assert division_list.is_right_open
    assert not division_list.is_right_closed

    assert not division_list.is_closed
    assert division_list.is_half_open
    assert division_list.is_half_closed