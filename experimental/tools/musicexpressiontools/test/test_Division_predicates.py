# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.Division import Division


def test_Division_predicates_01():

    division = Division((4, 8))

    assert division.is_left_closed
    assert not division.is_left_open

    assert division.is_right_closed
    assert not division.is_right_open

    assert division.is_closed
    assert not division.is_open

    assert not division.is_half_open
    assert not division.is_half_closed