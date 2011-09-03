from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_numbers_01():
    '''True when all elements in sequence are numbers.
    '''

    assert seqtools.all_are_numbers([1, 2, 5.5, Fraction(8, 3)])


def test_seqtools_all_are_numbers_02():
    '''True on empty sequence.
    '''

    assert seqtools.all_are_numbers([])


def test_seqtools_all_are_numbers_03():
    '''False otherwise.
    '''

    assert not seqtools.all_are_numbers([1, 2, pitchtools.NamedChromaticPitch(3)])


def test_seqtools_all_are_numbers_04():
    '''False when expr is not a sequence.
    '''

    assert not seqtools.all_are_numbers(17)
