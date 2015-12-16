# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_ResidueClass_operator_xor_01():
    r'''ResidueClass XOR ResidueClass returns a sieve.
    '''

    rc1 = sievetools.ResidueClass(4, 0)
    rc2 = sievetools.ResidueClass(4, 1)
    t = rc1 ^ rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert t.residue_classes == [rc1, rc2]


def test_sievetools_ResidueClass_operator_xor_02():
    r'''xor-sieve XOR ResidueClass returns a flat xor-sieve.
    '''

    sieve = sievetools.ResidueClass(4, 0) ^ sievetools.ResidueClass(4, 1)
    rc = sievetools.ResidueClass(3, 0)
    t = rc ^ sieve

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_xor_03():
    r'''ResidueClass XOR xor-sieve returns a flat xor-sieve.
    '''

    sieve = sievetools.ResidueClass(4, 0) ^ sievetools.ResidueClass(4, 1)
    rc = sievetools.ResidueClass(3, 0)
    t = sieve ^ rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_xor_04():
    r'''xor-sieve XOR xor-sieve returns a flat xor-sieve.
    '''

    rc1 = sievetools.ResidueClass(4, 0)
    rc2 = sievetools.ResidueClass(4, 1)
    rc3 = sievetools.ResidueClass(3, 0)
    rc4 = sievetools.ResidueClass(3, 1)
    rcsA = rc1 ^ rc2
    rcsB = rc3 ^ rc4
    t = rcsA ^ rcsB

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.residue_classes) == 4
    assert rc1 in t.residue_classes
    assert rc2 in t.residue_classes
    assert rc3 in t.residue_classes
    assert rc4 in t.residue_classes


def test_sievetools_ResidueClass_operator_xor_05():
    r'''XOR.
    '''

    residueclass = sievetools.ResidueClass(2, 0) ^ sievetools.ResidueClass(3, 0)

    assert isinstance(residueclass, sievetools.Sieve)
    assert residueclass.logical_operator == 'xor'
    assert residueclass.get_boolean_train(stop=6) == [0, 0, 1, 1, 1, 0]
    assert residueclass.get_congruent_bases(stop=6) == [2, 3, 4]


def test_sievetools_ResidueClass_operator_xor_06():
    r'''XOR.
    '''

    residueclass = sievetools.ResidueClass(2, 1) ^ sievetools.ResidueClass(3, 0)

    assert residueclass.get_boolean_train(stop=6) == [1, 1, 0, 0, 0, 1]
    assert residueclass.get_congruent_bases(stop=6) == [0, 1, 5, 6]