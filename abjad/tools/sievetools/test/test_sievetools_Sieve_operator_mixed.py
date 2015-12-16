# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_operator_mixed_01():
    r'''Mixed operators yield nested sieves.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    rc3 = sievetools.Sieve(3, 0)
    rc4 = sievetools.Sieve(3, 1)

    rcsA = rc1 & rc2
    rcsB = rc3 | rc4
    sieve = rcsA ^ rcsB

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'xor'
    assert len(sieve.residue_classes) == 2
    assert isinstance(sieve.residue_classes[0], sievetools.CompoundSieve)
    assert sieve.residue_classes[0].logical_operator == 'and'
    assert isinstance(sieve.residue_classes[1], sievetools.CompoundSieve)
    assert sieve.residue_classes[1].logical_operator == 'or'
    assert sieve.residue_classes[0] is rcsA
    assert sieve.residue_classes[1] is rcsB


def test_sievetools_Sieve_operator_mixed_02():
    r'''Mixed operators yield nested sieves.
    Sieves with the same operator, merge.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    rc3 = sievetools.Sieve(3, 0)
    rc4 = sievetools.Sieve(3, 1)

    rcsA = rc1 & rc2
    rcsB = rc3 | rc4
    sieve = rcsA | rcsB

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert len(sieve.residue_classes) == 3
    assert isinstance(sieve.residue_classes[0], sievetools.CompoundSieve)
    assert sieve.residue_classes[0].logical_operator == 'and'
    assert isinstance(sieve.residue_classes[1], sievetools.Sieve)
    assert isinstance(sieve.residue_classes[2], sievetools.Sieve)
    assert sieve.residue_classes[0] is rcsA
    assert sieve.residue_classes[1] is rc3
    assert sieve.residue_classes[2] is rc4


def test_sievetools_Sieve_operator_mixed_03():
    r'''Operators combined.
    '''

    sieve = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)
    sieve = sieve | sievetools.Sieve(3, 0)

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert len(sieve.residue_classes) == 2
    assert isinstance(sieve.residue_classes[0], sievetools.CompoundSieve)
    assert sieve.residue_classes[0].logical_operator == 'xor'
    assert isinstance(sieve.residue_classes[1], sievetools.Sieve)
    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [0, 2, 3, 4]


def test_sievetools_Sieve_operator_mixed_04():
    r'''Operators combined.
    '''

    sieve = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)
    sieve = sieve | sievetools.Sieve(3,0)

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert len(sieve.residue_classes) == 2
    assert isinstance(sieve.residue_classes[0], sievetools.CompoundSieve)
    assert sieve.residue_classes[0].logical_operator == 'xor'
    assert isinstance(sieve.residue_classes[1], sievetools.Sieve)
    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.congruent_bases == [0, 2, 3, 4]