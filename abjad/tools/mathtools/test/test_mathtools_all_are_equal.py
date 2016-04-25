# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_equal_01():
    r'''Is true when all elements in sequence are equal.
    '''

    assert mathtools.all_are_equal([-1, -1, -1, -1, -1])
    assert mathtools.all_are_equal([0, 0, 0, 0, 0])
    assert mathtools.all_are_equal([1, 1, 1, 1, 1])
    assert mathtools.all_are_equal([2, 2, 2, 2, 2])


def test_mathtools_all_are_equal_02():
    r'''True on empty sequence.
    '''

    assert mathtools.all_are_equal([])


def test_mathtools_all_are_equal_03():
    r'''Otherwise false.
    '''

    assert not mathtools.all_are_equal([-1, -1, -1, -1, 99])
    assert not mathtools.all_are_equal([0, 0, 0, 0, 99])
    assert not mathtools.all_are_equal([1, 1, 1, 1, 99])
    assert not mathtools.all_are_equal([2, 2, 2, 2, 99])


def test_mathtools_all_are_equal_04():
    r'''False when expr is not a sequence.
    '''

    assert not mathtools.all_are_equal(17)
