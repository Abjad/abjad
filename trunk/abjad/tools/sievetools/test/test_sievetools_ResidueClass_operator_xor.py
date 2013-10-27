# -*- encoding: utf-8 -*-
from abjad.tools import sievetools
from abjad.tools.sievetools import ResidueClass
import py.test


def test_sievetools_ResidueClass_operator_xor_01():
    r'''ResidueClass XOR ResidueClass returns a sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    t = rc1 ^ rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert t.rcs == [rc1, rc2]


def test_sievetools_ResidueClass_operator_xor_02():
    r'''xor-sieve XOR ResidueClass returns a flat xor-sieve.
    '''

    rcexpression = ResidueClass(4, 0) ^ ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = rc ^ rcexpression

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_sievetools_ResidueClass_operator_xor_03():
    r'''ResidueClass XOR xor-sieve returns a flat xor-sieve.
    '''

    rcexpression = ResidueClass(4, 0) ^ ResidueClass(4, 1)
    rc = ResidueClass(3, 0)
    t = rcexpression ^ rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_sievetools_ResidueClass_operator_xor_04():
    r'''xor-sieve XOR xor-sieve returns a flat xor-sieve.
    '''

    rc1 = ResidueClass(4, 0)
    rc2 = ResidueClass(4, 1)
    rc3 = ResidueClass(3, 0)
    rc4 = ResidueClass(3, 1)
    rcsA = rc1 ^ rc2
    rcsB = rc3 ^ rc4
    t = rcsA ^ rcsB

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.rcs) == 4
    assert rc1 in t.rcs
    assert rc2 in t.rcs
    assert rc3 in t.rcs
    assert rc4 in t.rcs


def test_sievetools_ResidueClass_operator_xor_05():
    r'''XOR.
    '''

    residueclass = ResidueClass(2, 0) ^ ResidueClass(3, 0)

    assert isinstance(residueclass, sievetools.Sieve)
    assert residueclass.logical_operator == 'xor'
    assert residueclass.get_boolean_train(6) == [0,0,1,1,1,0]
    assert residueclass.get_congruent_bases(6) == [2,3,4]


def test_sievetools_ResidueClass_operator_xor_06():
    r'''XOR.
    '''

    residueclass = ResidueClass(2, 1) ^ ResidueClass(3, 0)

    assert residueclass.get_boolean_train(6) == [1,1,0,0,0,1]
    assert residueclass.get_congruent_bases(6) == [0,1,5,6]
