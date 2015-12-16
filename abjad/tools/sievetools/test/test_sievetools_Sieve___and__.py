# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve___and___01():
    r'''Residue class AND residue class returns a sieve.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    compound_sieve = sieve_1 & sieve_2

    assert isinstance(compound_sieve, sievetools.CompoundSieve)
    assert compound_sieve.logical_operator == 'and'
    assert compound_sieve.sieves == [sieve_1, sieve_2]
    assert compound_sieve.boolean_train == [0, 0, 0, 0]
    assert compound_sieve.congruent_bases == []


def test_sievetools_Sieve___and___02():
    r'''and-sieve AND residue class returns a flat and-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) & sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    compound_sieve = rc & sieve

    assert isinstance(compound_sieve, sievetools.CompoundSieve)
    assert compound_sieve.logical_operator == 'and'
    assert len(compound_sieve.sieves) == 3
    assert sieve.sieves[0] in compound_sieve.sieves
    assert sieve.sieves[1] in compound_sieve.sieves
    assert rc in compound_sieve.sieves


def test_sievetools_Sieve___and___03():
    r'''residue class AND and-sieve returns a flat and-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) & sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    compound_sieve = sieve & rc

    assert isinstance(compound_sieve, sievetools.CompoundSieve)
    assert compound_sieve.logical_operator == 'and'
    assert len(compound_sieve.sieves) == 3
    assert sieve.sieves[0] in compound_sieve.sieves
    assert sieve.sieves[1] in compound_sieve.sieves
    assert rc in compound_sieve.sieves


def test_sievetools_Sieve___and___04():
    r'''and-sieve AND and-sieve returns a flat and-sieve.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve_3 = sievetools.Sieve(3, 0)
    sieve_4 = sievetools.Sieve(3, 1)
    rcsA = sieve_1 & sieve_2
    rcsB = sieve_3 & sieve_4
    compound_sieve = rcsA & rcsB

    assert isinstance(compound_sieve, sievetools.CompoundSieve)
    assert compound_sieve.logical_operator == 'and'
    assert len(compound_sieve.sieves) == 4
    assert sieve_1 in compound_sieve.sieves
    assert sieve_2 in compound_sieve.sieves
    assert sieve_3 in compound_sieve.sieves
    assert sieve_4 in compound_sieve.sieves


def test_sievetools_Sieve___and___05():
    r'''AND.
    '''

    residueclass = sievetools.Sieve(2, 0) & sievetools.Sieve(3, 0)

    assert isinstance(residueclass, sievetools.CompoundSieve)
    assert residueclass.logical_operator == 'and'
    assert residueclass.boolean_train == [1, 0, 0, 0, 0, 0]
    assert residueclass.congruent_bases == [0]


def test_sievetools_Sieve___and___06():
    r'''AND.
    '''

    residueclass = sievetools.Sieve(2, 1) 
    residueclass = residueclass & sievetools.Sieve(3, 0)

    assert residueclass.boolean_train == [0, 0, 0, 1, 0, 0]
    assert residueclass.congruent_bases == [3]