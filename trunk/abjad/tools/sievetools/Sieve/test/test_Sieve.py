# -*- encoding: utf-8 -*-
from abjad.tools import sievetools
from abjad.tools.sievetools import ResidueClass
import py.test


def test_Sieve_01():
    r'''Boolean operator defaults to OR.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 0), ResidueClass(3, 0)])

    assert sieve.logical_operator == 'or'


def test_Sieve_02():
    r'''Logical OR.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 0), ResidueClass(3, 0)])

    assert sieve.get_boolean_train(6) == [1, 0, 1, 1, 1, 0]
    assert sieve.get_congruent_bases(6) == [0, 2, 3, 4, 6]


def test_Sieve_03():
    r'''Logical OR.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 1), ResidueClass(3, 0)])

    assert sieve.get_boolean_train(6) == [1, 1, 0, 1, 0, 1]
    assert sieve.get_congruent_bases(6) == [0, 1, 3, 5, 6]


def test_Sieve_04():
    r'''Logical AND.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 0), ResidueClass(3, 0)], 'and')

    assert sieve.logical_operator == 'and'
    assert sieve.get_boolean_train(6) == [1, 0, 0, 0, 0, 0]
    assert sieve.get_congruent_bases(6) == [0, 6]


def test_Sieve_05():
    r'''Logical AND.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 1), ResidueClass(3, 0)], 'and')

    assert sieve.get_boolean_train(6) == [0, 0, 0, 1, 0, 0]
    assert sieve.get_congruent_bases(6) == [3]


def test_Sieve_06():
    r'''Logical XOR.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 0), ResidueClass(3, 0)], 'xor')

    assert sieve.logical_operator == 'xor'
    assert sieve.get_boolean_train(6) == [0, 0, 1, 1, 1, 0]
    assert sieve.get_congruent_bases(6) == [2, 3, 4]


def test_Sieve_07():
    r'''Logical XOR.
    '''

    sieve = sievetools.Sieve([ResidueClass(2, 1), ResidueClass(3, 0)], 'xor')

    assert sieve.get_boolean_train(6) == [1, 1, 0, 0, 0, 1]
    assert sieve.get_congruent_bases(6) == [0, 1, 5, 6]
