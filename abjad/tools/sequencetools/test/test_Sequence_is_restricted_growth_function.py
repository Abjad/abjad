# -*- coding: utf-8 -*-
from abjad import *


def test_Sequence_is_restricted_growth_function_01():

    assert Sequence((1, 1, 1, 1)).is_restricted_growth_function()
    assert Sequence((1, 1, 1, 2)).is_restricted_growth_function()
    assert Sequence((1, 1, 2, 1)).is_restricted_growth_function()
    assert Sequence((1, 1, 2, 2)).is_restricted_growth_function()
    assert Sequence((1, 1, 2, 3)).is_restricted_growth_function()
    assert Sequence((1, 2, 1, 1)).is_restricted_growth_function()
    assert Sequence((1, 2, 1, 2)).is_restricted_growth_function()
    assert Sequence((1, 2, 1, 3)).is_restricted_growth_function()
    assert Sequence((1, 2, 2, 1)).is_restricted_growth_function()
    assert Sequence((1, 2, 2, 2)).is_restricted_growth_function()
    assert Sequence((1, 2, 2, 3)).is_restricted_growth_function()
    assert Sequence((1, 2, 3, 1)).is_restricted_growth_function()
    assert Sequence((1, 2, 3, 2)).is_restricted_growth_function()
    assert Sequence((1, 2, 3, 3)).is_restricted_growth_function()
    assert Sequence((1, 2, 3, 4)).is_restricted_growth_function()


def test_Sequence_is_restricted_growth_function_02():

    assert not Sequence((1, 1, 1, 3)).is_restricted_growth_function()
    assert not Sequence((1, 1, 3, 3)).is_restricted_growth_function()
    assert not Sequence((1, 3, 1, 3)).is_restricted_growth_function()
    assert not Sequence((3, 1, 1, 3)).is_restricted_growth_function()
