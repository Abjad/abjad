# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_numbers_01():
    r'''True when all elements in sequence are numbers.
    '''

    assert sequencetools.all_are_numbers([1, 2, 5.5, Fraction(8, 3)])


def test_sequencetools_all_are_numbers_02():
    r'''True on empty sequence.
    '''

    assert sequencetools.all_are_numbers([])


def test_sequencetools_all_are_numbers_03():
    r'''Otherwise false.
    '''

    assert not sequencetools.all_are_numbers([1, 2, NamedPitch(3)])


def test_sequencetools_all_are_numbers_04():
    r'''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_numbers(17)
