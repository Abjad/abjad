# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_Sieve_from_boolean_patterns_01():
    r'''Single length-2 cycle token with period and residue list.
    '''

    #boolean_pattern = (6, [0, 4, 5])
    pattern = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    sieve = sievetools.Sieve.from_boolean_patterns([pattern])

    assert sieve.residue_classes == [
        sievetools.ResidueClass(6, 0),
        sievetools.ResidueClass(6, 4),
        sievetools.ResidueClass(6, 5),
        ]


def test_sievetools_Sieve_from_boolean_patterns_02():
    r'''Arbitrarily many cycle tokens.
    '''

    #boolean_pattern_1 = (6, [0, 4, 5])
    #boolean_pattern_2 = (10, [0, 1, 2])
    pattern_1 = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    pattern_2 = rhythmmakertools.BooleanPattern(indices=[0, 1, 2], period=10)
    sieve = sievetools.Sieve.from_boolean_patterns([pattern_1, pattern_2])

    assert sieve.residue_classes == [
        sievetools.ResidueClass(6, 0),
        sievetools.ResidueClass(6, 4),
        sievetools.ResidueClass(6, 5),
        sievetools.ResidueClass(10, 0),
        sievetools.ResidueClass(10, 1),
        sievetools.ResidueClass(10, 2),
        ]


def test_sievetools_Sieve_from_boolean_patterns_03():
    r'''Works with no cycle tokens.
    '''

    sieve = sievetools.Sieve.from_boolean_patterns([])
    assert sieve.residue_classes == []


def test_sievetools_Sieve_from_boolean_patterns_04():
    r'''Sieves count as cycle tokens in themselves.
    '''

    sieve = sievetools.ResidueClass(6, 0)
    sieve = sieve | sievetools.ResidueClass(6, 1)
    sieve = sievetools.Sieve.from_boolean_patterns([sieve])

    assert sieve.residue_classes == [
        sievetools.ResidueClass(6, 0),
        sievetools.ResidueClass(6, 1),
        ]