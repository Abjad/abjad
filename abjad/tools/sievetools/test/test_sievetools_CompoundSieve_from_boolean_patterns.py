# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_CompoundSieve_from_boolean_patterns_01():
    r'''Single length-2 boolean pattern with period and residue list.
    '''

    pattern = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    sieve = sievetools.CompoundSieve.from_boolean_patterns([pattern])

    assert sieve.residue_classes == [
        sievetools.ResidueClass(6, 0),
        sievetools.ResidueClass(6, 4),
        sievetools.ResidueClass(6, 5),
        ]


def test_sievetools_CompoundSieve_from_boolean_patterns_02():
    r'''Arbitrarily many boolean patterns.
    '''

    pattern_1 = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    pattern_2 = rhythmmakertools.BooleanPattern(indices=[0, 1, 2], period=10)
    sieve = sievetools.CompoundSieve.from_boolean_patterns([pattern_1, pattern_2])

    assert sieve.residue_classes == [
        sievetools.ResidueClass(6, 0),
        sievetools.ResidueClass(6, 4),
        sievetools.ResidueClass(6, 5),
        sievetools.ResidueClass(10, 0),
        sievetools.ResidueClass(10, 1),
        sievetools.ResidueClass(10, 2),
        ]


def test_sievetools_CompoundSieve_from_boolean_patterns_03():
    r'''Works with no boolean patterns.
    '''

    sieve = sievetools.CompoundSieve.from_boolean_patterns([])
    assert sieve.residue_classes == []