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
    assert residue_class.congruent_bases == [0]
    assert residue_class.boolean_train == [1, 0]


def test_sievetools_ResidueClass_05():

    residue_class = sievetools.ResidueClass(2, 1)

    assert residue_class.period == 2
    assert residue_class.offset == 1
    assert residue_class.congruent_bases == [1]
    assert residue_class.boolean_train == [0, 1]


def test_sievetools_ResidueClass_06():

    residue_class = sievetools.ResidueClass(3, 0)

    assert residue_class.period == 3
    assert residue_class.offset == 0
    assert residue_class.congruent_bases == [0]
    assert residue_class.boolean_train == [1, 0, 0]


def test_sievetools_ResidueClass_07():

    residue_class = sievetools.ResidueClass(3, 1)

    assert residue_class.period == 3
    assert residue_class.offset == 1
    assert residue_class.congruent_bases == [1]
    assert residue_class.boolean_train == [0, 1, 0]


def test_sievetools_ResidueClass_08():

    residue_class = sievetools.ResidueClass(1, 0)

    assert residue_class.congruent_bases == [0]
    assert residue_class.boolean_train == [1]