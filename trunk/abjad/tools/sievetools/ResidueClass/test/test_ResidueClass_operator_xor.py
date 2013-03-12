from abjad.tools import sievetools
from abjad.tools.sievetools import ResidueClass as RC
import py.test


def test_ResidueClass_operator_xor_01():
    '''RC XOR RC returns a sieve.
    '''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    t = rc1 ^ rc2

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert t.rcs == [rc1, rc2]


def test_ResidueClass_operator_xor_02():
    '''xor-sieve XOR RC returns a flat xor-sieve.
    '''

    rcexpression = RC(4, 0) ^ RC(4, 1)
    rc = RC(3, 0)
    t = rc ^ rcexpression

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_ResidueClass_operator_xor_03():
    '''RC XOR xor-sieve returns a flat xor-sieve.
    '''

    rcexpression = RC(4, 0) ^ RC(4, 1)
    rc = RC(3, 0)
    t = rcexpression ^ rc

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_ResidueClass_operator_xor_04():
    '''xor-sieve XOR xor-sieve returns a flat xor-sieve.
    '''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    rc3 = RC(3, 0)
    rc4 = RC(3, 1)
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


def test_ResidueClass_operator_xor_05():
    '''XOR.
    '''

    t = RC(2, 0) ^ RC(3, 0)

    assert isinstance(t, sievetools.Sieve)
    assert t.logical_operator == 'xor'
    assert t.get_boolean_train(6) == [0,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [2,3,4]


def test_ResidueClass_operator_xor_06():
    '''XOR.
    '''

    t = RC(2, 1) ^ RC(3, 0)

    assert t.get_boolean_train(6) == [1,1,0,0,0,1]
    assert t.get_congruent_bases(6) == [0,1,5,6]
