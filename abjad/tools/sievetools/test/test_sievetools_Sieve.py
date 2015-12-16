# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_01():
    r'''Boolean operator defaults to OR.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)])

    assert sieve.logical_operator == 'or'


def test_sievetools_Sieve_02():
    r'''Logical OR.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)])

    assert sieve.get_boolean_train() == [1, 0, 1, 1, 1, 0]
    assert sieve.get_congruent_bases() == [0, 2, 3, 4]


def test_sievetools_Sieve_03():
    r'''Logical OR.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)])

    assert sieve.get_boolean_train() == [1, 1, 0, 1, 0, 1]
    assert sieve.get_congruent_bases() == [0, 1, 3, 5]


def test_sievetools_Sieve_04():
    r'''Logical AND.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)], 'and')

    assert sieve.logical_operator == 'and'
    assert sieve.get_boolean_train() == [1, 0, 0, 0, 0, 0]
    assert sieve.get_congruent_bases() == [0]


def test_sievetools_Sieve_05():
    r'''Logical AND.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)], 'and')

    assert sieve.get_boolean_train() == [0, 0, 0, 1, 0, 0]
    assert sieve.get_congruent_bases() == [3]


def test_sievetools_Sieve_06():
    r'''Logical XOR.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)], 'xor')

    assert sieve.logical_operator == 'xor'
    assert sieve.get_boolean_train() == [0, 0, 1, 1, 1, 0]
    assert sieve.get_congruent_bases() == [2, 3, 4]


def test_sievetools_Sieve_07():
    r'''Logical XOR.
    '''

    sieve = sievetools.Sieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)], 'xor')

    assert sieve.get_boolean_train() == [1, 1, 0, 0, 0, 1]
    assert sieve.get_congruent_bases() == [0, 1, 5]