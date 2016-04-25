# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_numbers_01():
    r'''Is true when all elements in sequence are numbers.
    '''

    assert mathtools.all_are_numbers([1, 2, 5.5, Fraction(8, 3)])


def test_mathtools_all_are_numbers_02():
    r'''True on empty sequence.
    '''

    assert mathtools.all_are_numbers([])


def test_mathtools_all_are_numbers_03():
    r'''Otherwise false.
    '''

    assert not mathtools.all_are_numbers([1, 2, NamedPitch(3)])


def test_mathtools_all_are_numbers_04():
    r'''False when expr is not a sequence.
    '''

    assert not mathtools.all_are_numbers(17)
