from abjad.tools import sievetools
from abjad.tools.sievetools.ResidueClass import ResidueClass
import py.test


RC = ResidueClass

def test_ResidueClass_01():
    '''modulo must be positive.'''

    py.test.raises(ValueError, 't = RC(0, 1)')


def test_ResidueClass_02():
    '''residue must be non-negative and < modulo.'''

    py.test.raises(ValueError, 't = RC(2, 13)')
    py.test.raises(ValueError, 't = RC(2, 2)')
    py.test.raises(ValueError, 't = RC(2, -1)')


def test_ResidueClass_03():
    '''modulo may be 1.'''

    t = RC(1, 0)

    assert t.modulo == 1
    assert t.residue == 0


def test_ResidueClass_04():

    t = RC(2, 0)

    assert t.modulo == 2
    assert t.residue == 0
    assert t.get_congruent_bases(4) == [0,2,4]
    assert t.get_boolean_train(4) == [1,0,1,0]


def test_ResidueClass_05():

    t = RC(2, 1)

    assert t.modulo == 2
    assert t.residue == 1
    assert t.get_congruent_bases(5) == [1,3,5]
    assert t.get_boolean_train(4) == [0,1,0,1]


def test_ResidueClass_06():

    t = RC(3, 0)

    assert t.modulo == 3
    assert t.residue == 0
    assert t.get_congruent_bases(6) == [0, 3, 6]
    assert t.get_boolean_train(6) == [1,0,0,1,0,0]


def test_ResidueClass_07():

    t = RC(3, 1)

    assert t.modulo == 3
    assert t.residue == 1
    assert t.get_congruent_bases(7) == [1, 4, 7]
    assert t.get_boolean_train(6) == [0,1,0,0,1,0]


def test_ResidueClass_08():
    '''get_congruent_bases() and get_boolean_train() must take
    range parameters.'''

    t = RC(1, 0)

    py.test.raises(AttributeError, 't = t. get_congruent_bases()')
    py.test.raises(AttributeError, 't = t. get_boolean_train()')

    assert isinstance(t.get_congruent_bases(12), list)
    assert isinstance(t.get_boolean_train(12), list)

    assert t.get_congruent_bases(99) == range(100)
    assert t.get_congruent_bases(-10, 99) == range(-10, 100)

    assert t.get_boolean_train(12) == [1] * 12
    assert t.get_boolean_train(-2, 12) == [1] * 14
