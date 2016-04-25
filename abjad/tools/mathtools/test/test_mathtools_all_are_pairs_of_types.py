# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_pairs_of_types_01():

    assert mathtools.all_are_pairs_of_types([('a', 1), ('b', 2), ('c', 3), ('derp', 666)], str, int)
    assert mathtools.all_are_pairs_of_types([], str, int)


def test_mathtools_all_are_pairs_of_types_02():

    assert not mathtools.all_are_pairs_of_types('foo', str, int)
    assert not mathtools.all_are_pairs_of_types(1.5, str, int)
    assert not mathtools.all_are_pairs_of_types([1, 2], str, int)
    assert not mathtools.all_are_pairs_of_types([(1, 2), (3, 4), (5, 6, 7)], str, int)
    assert not mathtools.all_are_pairs_of_types([('a', 1.1), ('b', 2.3), ('c', 3.5)], str, int)
    assert not mathtools.all_are_pairs_of_types([('a', 1), ('b', 2), ('c', 3.3)], str, int)
