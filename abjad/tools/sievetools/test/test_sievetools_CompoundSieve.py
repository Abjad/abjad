# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_CompoundSieve_01():
    r'''Boolean operator defaults to OR.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)])

    assert sieve.logical_operator == 'or'


def test_sievetools_CompoundSieve_02():
    r'''Logical OR.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)])

    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [0, 2, 3, 4]


def test_sievetools_CompoundSieve_03():
    r'''Logical OR.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)])

    assert sieve.boolean_train == [1, 1, 0, 1, 0, 1]
    assert sieve.congruent_bases == [0, 1, 3, 5]


def test_sievetools_CompoundSieve_04():
    r'''Logical AND.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)], 'and')

    assert sieve.logical_operator == 'and'
    assert sieve.boolean_train == [1, 0, 0, 0, 0, 0]
    assert sieve.congruent_bases == [0]


def test_sievetools_CompoundSieve_05():
    r'''Logical AND.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)], 'and')

    assert sieve.boolean_train == [0, 0, 0, 1, 0, 0]
    assert sieve.congruent_bases == [3]


def test_sievetools_CompoundSieve_06():
    r'''Logical XOR.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 0), sievetools.ResidueClass(3, 0)], 'xor')

    assert sieve.logical_operator == 'xor'
    assert sieve.boolean_train == [0, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [2, 3, 4]


def test_sievetools_CompoundSieve_07():
    r'''Logical XOR.
    '''

    sieve = sievetools.CompoundSieve([sievetools.ResidueClass(2, 1), sievetools.ResidueClass(3, 0)], 'xor')

    assert sieve.boolean_train == [1, 1, 0, 0, 0, 1]
    assert sieve.congruent_bases == [0, 1, 5]