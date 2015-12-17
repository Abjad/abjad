# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_Sieve___xor___01():

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    compound_sieve = sieve_1 ^ sieve_2

    assert compound_sieve.logical_operator == 'xor'
    assert compound_sieve.sieves == [sieve_1, sieve_2]


def test_sievetools_Sieve___xor___02():

    compound_sieve_1 = sievetools.Sieve(4, 0) ^ sievetools.Sieve(4, 1)
    sieve = sievetools.Sieve(3, 0)
    compound_sieve_2 = sieve ^ compound_sieve_1

    assert compound_sieve_2.logical_operator == 'xor'
    assert len(compound_sieve_2.sieves) == 3
    assert compound_sieve_1.sieves[0] in compound_sieve_2.sieves
    assert compound_sieve_1.sieves[1] in compound_sieve_2.sieves
    assert sieve in compound_sieve_2.sieves


def test_sievetools_Sieve___xor___03():

    compound_sieve_1 = sievetools.Sieve(4, 0) ^ sievetools.Sieve(4, 1)
    sieve = sievetools.Sieve(3, 0)
    compound_sieve_2 = compound_sieve_1 ^ sieve

    assert compound_sieve_2.logical_operator == 'xor'
    assert len(compound_sieve_2.sieves) == 3
    assert compound_sieve_1.sieves[0] in compound_sieve_2.sieves
    assert compound_sieve_1.sieves[1] in compound_sieve_2.sieves
    assert sieve in compound_sieve_2.sieves


def test_sievetools_Sieve___xor___04():

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve_3 = sievetools.Sieve(3, 0)
    sieve_4 = sievetools.Sieve(3, 1)
    compound_sieve_1 = sieve_1 ^ sieve_2
    compound_sieve_2 = sieve_3 ^ sieve_4
    compound_sieve_3 = compound_sieve_1 ^ compound_sieve_2

    assert compound_sieve_3.logical_operator == 'xor'
    assert len(compound_sieve_3.sieves) == 4
    assert sieve_1 in compound_sieve_3.sieves
    assert sieve_2 in compound_sieve_3.sieves
    assert sieve_3 in compound_sieve_3.sieves
    assert sieve_4 in compound_sieve_3.sieves


def test_sievetools_Sieve___xor___05():

    compound_sieve = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)

    assert compound_sieve.logical_operator == 'xor'
    assert compound_sieve.boolean_train == [0, 0, 1, 1, 1, 0]
    assert compound_sieve.congruent_bases == [2, 3, 4]


def test_sievetools_Sieve___xor___06():

    compound_sieve = sievetools.Sieve(2, 1) ^ sievetools.Sieve(3, 0)

    assert compound_sieve.boolean_train == [1, 1, 0, 0, 0, 1]
    assert compound_sieve.congruent_bases == [0, 1, 5]