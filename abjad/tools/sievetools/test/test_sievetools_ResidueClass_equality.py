# -*- encoding: utf-8 -*-
from abjad.tools import sievetools
from abjad.tools.sievetools.ResidueClass import ResidueClass
from abjad.tools.sievetools.Sieve import Sieve
import pytest


RC = ResidueClass

def test_sievetools_ResidueClass_equality_01():
    r'''non-equal residue classes
    '''

    t1 = RC(2, 1)
    t2 = RC(3, 1)

    assert t1 != t2


def test_sievetools_ResidueClass_equality_02():
    r'''non-equal objects
    '''

    rc = RC(2, 1)

    assert rc != 'a'
    assert 2 != rc


def test_sievetools_ResidueClass_equality_03():
    r'''equal
    '''

    t1 = RC(2, 1)
    t2 = RC(2, 1)

    assert t1 == t2
