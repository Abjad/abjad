# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.sievetools import ResidueClass
import pytest


def test_sievetools_ResidueClass_operator_or_01():
    r'''ResidueClass OR ResidueClass returns a sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    t = rc1 | rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'or'
    assert t.residue_classes == [rc1, rc2]


def test_sievetools_ResidueClass_operator_or_02():
    r'''or-Sieve OR ResidueClass returns a flat or-sieve.
    '''

    sieve = ResidueClass(4, 0) | ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = rc | sieve

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'or'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_or_03():
    r'''ResidueClass OR or-sieve returns a flat or-sieve.
    '''

    sieve = ResidueClass(4, 0) | ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = sieve | rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'or'
    assert len(t.residue_classes) == 3
    assert sieve.residue_classes[0] in t.residue_classes
    assert sieve.residue_classes[1] in t.residue_classes
    assert rc in t.residue_classes


def test_sievetools_ResidueClass_operator_or_04():
    r'''or-sieve OR or-Sieve returns a flat or-sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    rc3 = ResidueClass(3, 0)
    rc4 = ResidueClass(3, 1)
    rcsA = rc1 | rc2
    rcsB = rc3 | rc4
    t = rcsA | rcsB

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'or'
    assert len(t.residue_classes) == 4
    assert rc1 in t.residue_classes
    assert rc2 in t.residue_classes
    assert rc3 in t.residue_classes
    assert rc4 in t.residue_classes


def test_sievetools_ResidueClass_operator_or_05():
    r'''OR.
    '''

    residueclass = ResidueClass(2, 0) | ResidueClass(3, 0)

    assert isinstance(residueclass, sievetools.Sieve)
    assert residueclass.logical_operator == 'or'
    assert residueclass.get_boolean_train(6) == [1,0,1,1,1,0]
    assert residueclass.get_congruent_bases(6) == [0,2,3,4,6]


def test_sievetools_ResidueClass_operator_or_06():
    r'''OR.
    '''

    residueclass = ResidueClass(2, 1) | ResidueClass(3, 0)

    assert residueclass.get_boolean_train(6) == [1,1,0,1,0,1]
    assert residueclass.get_congruent_bases(6) == [0,1,3,5,6]