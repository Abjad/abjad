# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_operators_01():
    r'''Mixed operators yield nested sieves.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve_3 = sievetools.Sieve(3, 0)
    sieve_4 = sievetools.Sieve(3, 1)

    rcsA = sieve_1 & sieve_2
    rcsB = sieve_3 | sieve_4
    sieve = rcsA ^ rcsB

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'xor'
    assert len(sieve.sieves) == 2
    assert isinstance(sieve.sieves[0], sievetools.CompoundSieve)
    assert sieve.sieves[0].logical_operator == 'and'
    assert isinstance(sieve.sieves[1], sievetools.CompoundSieve)
    assert sieve.sieves[1].logical_operator == 'or'
    assert sieve.sieves[0] is rcsA
    assert sieve.sieves[1] is rcsB


def test_sievetools_Sieve_operators_02():
    r'''Mixed operators yield nested sieves.
    Sieves with the same operator, merge.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve_3 = sievetools.Sieve(3, 0)
    sieve_4 = sievetools.Sieve(3, 1)

    rcsA = sieve_1 & sieve_2
    rcsB = sieve_3 | sieve_4
    sieve = rcsA | rcsB

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert len(sieve.sieves) == 3
    assert isinstance(sieve.sieves[0], sievetools.CompoundSieve)
    assert sieve.sieves[0].logical_operator == 'and'
    assert isinstance(sieve.sieves[1], sievetools.Sieve)
    assert isinstance(sieve.sieves[2], sievetools.Sieve)
    assert sieve.sieves[0] is rcsA
    assert sieve.sieves[1] is sieve_3
    assert sieve.sieves[2] is sieve_4


def test_sievetools_Sieve_operators_03():

    sieve = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)
    sieve = sieve | sievetools.Sieve(3, 0)

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert len(sieve.sieves) == 2
    assert isinstance(sieve.sieves[0], sievetools.CompoundSieve)
    assert sieve.sieves[0].logical_operator == 'xor'
    assert isinstance(sieve.sieves[1], sievetools.Sieve)
    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [0, 2, 3, 4]


def test_sievetools_Sieve_operators_04():

    sieve = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)
    sieve = sieve | sievetools.Sieve(3,0)

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert len(sieve.sieves) == 2
    assert isinstance(sieve.sieves[0], sievetools.CompoundSieve)
    assert sieve.sieves[0].logical_operator == 'xor'
    assert isinstance(sieve.sieves[1], sievetools.Sieve)
    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [0, 2, 3, 4]