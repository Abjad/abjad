from abjad.tools import sievetools
from abjad.tools.sievetools.ResidueClass import ResidueClass
from abjad.tools.sievetools.Sieve import Sieve
import py.test


RC = ResidueClass

def test_ResidueClass_operator_or_01():
    '''RC OR RC returns a Sieve.'''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    t = rc1 | rc2

    assert isinstance(t, Sieve)
    assert t.operator == 'or'
    assert t.rcs == [rc1, rc2]


def test_ResidueClass_operator_or_02():
    '''or-Sieve OR RC returns a flat or-Sieve.'''

    rcexpression = RC(4, 0) | RC(4, 1)
    rc = RC(3, 0)
    t = rc | rcexpression

    assert isinstance(t, Sieve)
    assert t.operator == 'or'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_ResidueClass_operator_or_03():
    '''RC OR or-Sieve returns a flat or-Sieve.'''

    rcexpression = RC(4, 0) | RC(4, 1)
    rc = RC(3, 0)
    t = rcexpression | rc

    assert isinstance(t, Sieve)
    assert t.operator == 'or'
    assert len(t.rcs) == 3
    assert rcexpression.rcs[0] in t.rcs
    assert rcexpression.rcs[1] in t.rcs
    assert rc in t.rcs


def test_ResidueClass_operator_or_04():
    '''or-Sieve OR or-Sieve returns a flat or-Sieve.'''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    rc3 = RC(3, 0)
    rc4 = RC(3, 1)
    rcsA = rc1 | rc2
    rcsB = rc3 | rc4
    t = rcsA | rcsB

    assert isinstance(t, Sieve)
    assert t.operator == 'or'
    assert len(t.rcs) == 4
    assert rc1 in t.rcs
    assert rc2 in t.rcs
    assert rc3 in t.rcs
    assert rc4 in t.rcs


def test_ResidueClass_operator_or_05():
    '''OR'''

    t = RC(2, 0) | RC(3, 0)

    assert isinstance(t, Sieve)
    assert t.operator == 'or'
    assert t.get_boolean_train(6) == [1,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_ResidueClass_operator_or_06():
    '''OR'''

    t = RC(2, 1) | RC(3, 0)

    assert t.get_boolean_train(6) == [1,1,0,1,0,1]
    assert t.get_congruent_bases(6) == [0,1,3,5,6]
