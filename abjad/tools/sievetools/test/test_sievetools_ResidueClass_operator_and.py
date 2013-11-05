# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.sievetools import ResidueClass
import py.test


def test_sievetools_ResidueClass_operator_and_01():
    r'''Residue class AND residue class returns a sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    t = rc1 & rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert t.rcs == [rc1, rc2]
    assert t.get_boolean_train(4) == [0,0,0,0]
    assert t.get_congruent_bases(6) == []


def test_sievetools_ResidueClass_operator_and_02():
    r'''and-sieve AND residue class returns a flat and-sieve.
    '''

    rcexpression = ResidueClass(4, 0) & ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = rc & rcexpression

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_sievetools_ResidueClass_operator_and_03():
    r'''residue class AND and-sieve returns a flat and-sieve.
    '''

    rcexpression = ResidueClass(4, 0) & ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = rcexpression & rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_sievetools_ResidueClass_operator_and_04():
    r'''and-sieve AND and-sieve returns a flat and-sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    rc3 = ResidueClass(3, 0)
    rc4 = ResidueClass(3, 1)
    rcsA = rc1 & rc2
    rcsB = rc3 & rc4
    t = rcsA & rcsB

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'and'
    assert len(t.rcs) == 4
    assert rc1 in t.rcs
    assert rc2 in t.rcs
    assert rc3 in t.rcs
    assert rc4 in t.rcs


def test_sievetools_ResidueClass_operator_and_05():
    r'''AND.
    '''

    residueclass = ResidueClass(2, 0) & ResidueClass(3, 0)

    assert isinstance(residueclass, sievetools.Sieve)
    assert residueclass.logical_operator == 'and'
    assert residueclass.get_boolean_train(6) == [1,0,0,0,0,0]
    assert residueclass.get_congruent_bases(6) == [0, 6]


def test_sievetools_ResidueClass_operator_and_06():
    r'''AND.
    '''

    residueclass = ResidueClass(2, 1) & ResidueClass(3, 0)

    assert residueclass.get_boolean_train(6) == [0,0,0,1,0,0]
    assert residueclass.get_congruent_bases(6) == [3]
