# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve___or___01():
    r'''Sieve OR Sieve returns a sieve.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve = sieve_1 | sieve_2

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert sieve.sieves == [sieve_1, sieve_2]


def test_sievetools_Sieve___or___02():
    r'''or-CompoundSieve OR Sieve returns a flat or-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) | sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    sieve = rc | sieve

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert len(sieve.sieves) == 3
    assert sieve.sieves[0] in sieve.sieves
    assert sieve.sieves[1] in sieve.sieves
    assert rc in sieve.sieves


def test_sievetools_Sieve___or___03():
    r'''Sieve OR or-sieve returns a flat or-sieve.
    '''

    sieve = sievetools.Sieve(4, 0) | sievetools.Sieve(4, 1)
    rc = sievetools.Sieve(3, 0)
    sieve = sieve | rc

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert len(sieve.sieves) == 3
    assert sieve.sieves[0] in sieve.sieves
    assert sieve.sieves[1] in sieve.sieves
    assert rc in sieve.sieves


def test_sievetools_Sieve___or___04():
    r'''or-sieve OR or-CompoundSieve returns a flat or-sieve.
    '''

    sieve_1 = sievetools.Sieve(4, 0)
    sieve_2 = sievetools.Sieve(4, 1)
    sieve_3 = sievetools.Sieve(3, 0)
    sieve_4 = sievetools.Sieve(3, 1)
    rcsA = sieve_1 | sieve_2
    rcsB = sieve_3 | sieve_4
    sieve = rcsA | rcsB

    assert isinstance(sieve, sievetools.CompoundSieve)
    assert sieve.logical_operator == 'or'
    assert len(sieve.sieves) == 4
    assert sieve_1 in sieve.sieves
    assert sieve_2 in sieve.sieves
    assert sieve_3 in sieve.sieves
    assert sieve_4 in sieve.sieves


def test_sievetools_Sieve___or___05():
    r'''OR.
    '''

    residueclass = sievetools.Sieve(2, 0) 
    residueclass = residueclass | sievetools.Sieve(3, 0)

    assert isinstance(residueclass, sievetools.CompoundSieve)
    assert residueclass.logical_operator == 'or'
    assert residueclass.boolean_train == [1, 0, 1, 1, 1, 0]
    assert residueclass.congruent_bases == [0, 2, 3, 4]


def test_sievetools_Sieve___or___06():
    r'''OR.
    '''

    residueclass = sievetools.Sieve(2, 1) 
    residueclass = residueclass | sievetools.Sieve(3, 0)

    assert residueclass.boolean_train == [1, 1, 0, 1, 0, 1]
    assert residueclass.congruent_bases == [0, 1, 3, 5]