# -*- coding: utf-8 -*-
import pytest
from abjad.tools import *
from abjad.tools import sievetools


def test_sievetools_ResidueClass_01():
    r'''period must be positive.
    '''

    pytest.raises(ValueError, 't = sievetools.ResidueClass(0, 1)')


def test_sievetools_ResidueClass_02():
    r'''residue must be non-negative and < period.
    '''

    pytest.raises(ValueError, 't = sievetools.ResidueClass(2, 13)')
    pytest.raises(ValueError, 't = sievetools.ResidueClass(2, 2)')
    pytest.raises(ValueError, 't = sievetools.ResidueClass(2, -1)')


def test_sievetools_ResidueClass_03():
    r'''period may be 1.
    '''

    residue_class = sievetools.ResidueClass(1, 0)

    assert residue_class.period == 1
    assert residue_class.offset == 0


def test_sievetools_ResidueClass_04():

    residue_class = sievetools.ResidueClass(2, 0)

    assert residue_class.period == 2
    assert residue_class.offset == 0
    assert residue_class.get_congruent_bases(stop=4) == [0, 2]
    assert residue_class.get_boolean_train(stop=4) == [1, 0, 1, 0]


def test_sievetools_ResidueClass_05():

    residue_class = sievetools.ResidueClass(2, 1)

    assert residue_class.period == 2
    assert residue_class.offset == 1
    assert residue_class.get_congruent_bases(stop=5) == [1, 3]
    assert residue_class.get_boolean_train(stop=4) == [0, 1, 0, 1]


def test_sievetools_ResidueClass_06():

    residue_class = sievetools.ResidueClass(3, 0)

    assert residue_class.period == 3
    assert residue_class.offset == 0
    assert residue_class.get_congruent_bases(stop=6) == [0, 3]
    assert residue_class.get_boolean_train(stop=6) == [1, 0, 0, 1, 0, 0]


def test_sievetools_ResidueClass_07():

    residue_class = sievetools.ResidueClass(3, 1)

    assert residue_class.period == 3
    assert residue_class.offset == 1
    assert residue_class.get_congruent_bases(stop=7) == [1, 4]
    assert residue_class.get_boolean_train(stop=6) == [0, 1, 0, 0, 1, 0]


def test_sievetools_ResidueClass_08():
    r'''The get_congruent_bases() and get_boolean_train() methods must take
    range parameters.
    '''

    residue_class = sievetools.ResidueClass(1, 0)

    assert isinstance(residue_class.get_congruent_bases(stop=12), list)
    assert isinstance(residue_class.get_boolean_train(stop=12), list)

    assert residue_class.get_congruent_bases(stop=99) == list(range(99))
    assert residue_class.get_congruent_bases(-10, 99) == list(range(-10, 99))

    assert residue_class.get_boolean_train(stop=12) == [1] * 12
    assert residue_class.get_boolean_train(start=-2, stop=12) == [1] * 14