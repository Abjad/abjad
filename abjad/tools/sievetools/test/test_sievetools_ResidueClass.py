# -*- encoding: utf-8 -*-
import pytest
from abjad.tools.sievetools.ResidueClass import ResidueClass


RC = ResidueClass

def test_sievetools_ResidueClass_01():
    r'''modulo must be positive.
    '''

    pytest.raises(ValueError, 't = RC(0, 1)')


def test_sievetools_ResidueClass_02():
    r'''residue must be non-negative and < modulo.
    '''

    pytest.raises(ValueError, 't = RC(2, 13)')
    pytest.raises(ValueError, 't = RC(2, 2)')
    pytest.raises(ValueError, 't = RC(2, -1)')


def test_sievetools_ResidueClass_03():
    r'''modulo may be 1.
    '''

    rc = RC(1, 0)

    assert rc.modulo == 1
    assert rc.residue == 0


def test_sievetools_ResidueClass_04():

    rc = RC(2, 0)

    assert rc.modulo == 2
    assert rc.residue == 0
    assert rc.get_congruent_bases(4) == [0,2,4]
    assert rc.get_boolean_train(4) == [1,0,1,0]


def test_sievetools_ResidueClass_05():

    rc = RC(2, 1)

    assert rc.modulo == 2
    assert rc.residue == 1
    assert rc.get_congruent_bases(5) == [1,3,5]
    assert rc.get_boolean_train(4) == [0,1,0,1]


def test_sievetools_ResidueClass_06():

    rc = RC(3, 0)

    assert rc.modulo == 3
    assert rc.residue == 0
    assert rc.get_congruent_bases(6) == [0, 3, 6]
    assert rc.get_boolean_train(6) == [1,0,0,1,0,0]


def test_sievetools_ResidueClass_07():

    rc = RC(3, 1)

    assert rc.modulo == 3
    assert rc.residue == 1
    assert rc.get_congruent_bases(7) == [1, 4, 7]
    assert rc.get_boolean_train(6) == [0,1,0,0,1,0]


def test_sievetools_ResidueClass_08():
    r'''get_congruent_bases() and get_boolean_train() must take
    range parameters.'''

    rc = RC(1, 0)

    pytest.raises(Exception, 'rc = rc. get_congruent_bases()')
    pytest.raises(Exception, 'rc = rc. get_boolean_train()')

    assert isinstance(rc.get_congruent_bases(12), list)
    assert isinstance(rc.get_boolean_train(12), list)

    assert rc.get_congruent_bases(99) == range(100)
    assert rc.get_congruent_bases(-10, 99) == range(-10, 100)

    assert rc.get_boolean_train(12) == [1] * 12
    assert rc.get_boolean_train(-2, 12) == [1] * 14
