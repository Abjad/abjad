# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_operator_and_01():
    r'''Residue class AND residue class returns a sieve.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    t = rc1 & rc2

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'and'
    assert t.residue_classes == [rc1, rc2]
    assert t.boolean_train == [0, 0, 0, 0]
    assert t.congruent_bases == []


def test_sievetools_Sieve_operator_and_02():
    r'''and-sieve AND residue class returns a flat and-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) & sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    t = rc & sieve

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_Sieve_operator_and_03():
    r'''residue class AND and-sieve returns a flat and-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) & sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    t = sieve & rc

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_Sieve_operator_and_04():
    r'''and-sieve AND and-sieve returns a flat and-sieve.
    '''

    rc1 = sievetools.Sieve(4, 0)
    rc2 = sievetools.Sieve(4, 1)
    rc3 = sievetools.Sieve(3, 0)
    rc4 = sievetools.Sieve(3, 1)
    rcsA = rc1 & rc2
    rcsB = rc3 & rc4
    t = rcsA & rcsB

    assert isinstance(t, sievetools.CompoundSieve)
    assert t.logical_operator == 'and'
    assert len(t.residue_classes) == 4
    assert rc1 in t.residue_classes
    assert rc2 in t.residue_classes
    assert rc3 in t.residue_classes
    assert rc4 in t.residue_classes


def test_sievetools_Sieve_operator_and_05():
    r'''AND.
    '''

    residueclass = sievetools.Sieve(2, 0) & sievetools.Sieve(3, 0)

    assert isinstance(residueclass, sievetools.CompoundSieve)
    assert residueclass.logical_operator == 'and'
    assert residueclass.boolean_train == [1, 0, 0, 0, 0, 0]
    assert residueclass.congruent_bases == [0]


def test_sievetools_Sieve_operator_and_06():
    r'''AND.
    '''

    residueclass = sievetools.Sieve(2, 1) 
    residueclass = residueclass & sievetools.Sieve(3, 0)

    assert residueclass.boolean_train == [0, 0, 0, 1, 0, 0]
    assert residueclass.congruent_bases == [3]