# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_operator_xor_01():
    r'''Sieve XOR Sieve returns a sieve.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    t = rc1 ^ rc2

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'xor'
    assert t.residue_classes == [rc1, rc2]


def test_sievetools_Sieve_operator_xor_02():
    r'''xor-sieve XOR Sieve returns a flat xor-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) ^ sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    t = rc ^ sieve

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_Sieve_operator_xor_03():
    r'''Sieve XOR xor-sieve returns a flat xor-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) ^ sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    t = sieve ^ rc

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_Sieve_operator_xor_04():
    r'''xor-sieve XOR xor-sieve returns a flat xor-sieve.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    rc3 = sievetools.Sieve(3, 0)
    rc4 = sievetools.Sieve(3, 1)
    rcsA = rc1 ^ rc2
    rcsB = rc3 ^ rc4
    t = rcsA ^ rcsB

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 4
    assert rc1 in t.residue_classes
    assert rc2 in t.residue_classes
    assert rc3 in t.residue_classes
    assert rc4 in t.residue_classes


def test_sievetools_Sieve_operator_xor_05():
    r'''XOR.
    '''

    residueclass = sievetools.Sieve(2, 0) ^ sievetools.Sieve(3, 0)

    assert isinstance(residueclass, sievetools.CompoundSieve)
    assert residueclass.logical_operator == 'xor'
    assert residueclass.boolean_train == [0, 0, 1, 1, 1, 0]
    assert residueclass.congruent_bases == [2, 3, 4]


def test_sievetools_Sieve_operator_xor_06():
    r'''XOR.
    '''

    residueclass = sievetools.Sieve(2, 1) ^ sievetools.Sieve(3, 0)

    assert residueclass.boolean_train == [1, 1, 0, 0, 0, 1]
    assert residueclass.congruent_bases == [0, 1, 5]