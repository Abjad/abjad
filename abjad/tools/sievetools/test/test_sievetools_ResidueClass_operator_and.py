# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools
import pytest


def test_sievetools_ResidueClass_operator_and_01():
    r'''Residue class AND residue class returns a sieve.
    '''

    rc1 = sievetools.ResidueClass(4, 0)
    rc2 = sievetools.ResidueClass(4, 1)
    t = rc1 & rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert t.residue_classes == [rc1, rc2]
    assert t.get_boolean_train(stop=4) == [0, 0, 0, 0]
    assert t.get_congruent_bases(6) == []


def test_sievetools_ResidueClass_operator_and_02():
    r'''and-sieve AND residue class returns a flat and-sieve.
    '''

    sieve = sievetools.ResidueClass(4, 0) & sievetools.ResidueClass(4, 1)
    rc = sievetools.ResidueClass(3, 0)
    t = rc & sieve

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_and_03():
    r'''residue class AND and-sieve returns a flat and-sieve.
    '''

    sieve = sievetools.ResidueClass(4, 0) & sievetools.ResidueClass(4, 1)
    rc = sievetools.ResidueClass(3, 0)
    t = sieve & rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_and_04():
    r'''and-sieve AND and-sieve returns a flat and-sieve.
    '''

    rc1 = sievetools.ResidueClass(4, 0)
    rc2 = sievetools.ResidueClass(4, 1)
    rc3 = sievetools.ResidueClass(3, 0)
    rc4 = sievetools.ResidueClass(3, 1)
    rcsA = rc1 & rc2
    rcsB = rc3 & rc4
    t = rcsA & rcsB

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 4
    assert rc1 in t.residue_classes
    assert rc2 in t.residue_classes
    assert rc3 in t.residue_classes
    assert rc4 in t.residue_classes


def test_sievetools_ResidueClass_operator_and_05():
    r'''AND.
    '''

    residueclass = sievetools.ResidueClass(2, 0) & sievetools.ResidueClass(3, 0)

    assert isinstance(residueclass, sievetools.Sieve)
    assert residueclass.logical_operator == 'and'
    assert residueclass.get_boolean_train(stop=6) == [1, 0, 0, 0, 0, 0]
    assert residueclass.get_congruent_bases(6) == [0, 6]


def test_sievetools_ResidueClass_operator_and_06():
    r'''AND.
    '''

    residueclass = sievetools.ResidueClass(2, 1) & sievetools.ResidueClass(3, 0)

    assert residueclass.get_boolean_train(stop=6) == [0, 0, 0, 1, 0, 0]
    assert residueclass.get_congruent_bases(6) == [3]