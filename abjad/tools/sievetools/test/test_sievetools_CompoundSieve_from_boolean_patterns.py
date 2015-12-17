# -*- coding: utf-8 -*-
from abjad import *


def test_sievetools_CompoundSieve_from_boolean_patterns_01():
    r'''From one boolean pattern.
    '''

    pattern = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    compound_sieve = sievetools.CompoundSieve.from_boolean_patterns([pattern])

    assert compound_sieve.sieves == [
        sievetools.Sieve(6, 0),
        sievetools.Sieve(6, 4),
        sievetools.Sieve(6, 5),
        ]


def test_sievetools_CompoundSieve_from_boolean_patterns_02():
    r'''From multiple boolean patterns.
    '''

    pattern_1 = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    pattern_2 = rhythmmakertools.BooleanPattern(indices=[0, 1, 2], period=10)
    patterns = [pattern_1, pattern_2]
    compound_sieve = sievetools.CompoundSieve.from_boolean_patterns(patterns)

    assert compound_sieve.sieves == [
        sievetools.Sieve(6, 0),
        sievetools.Sieve(6, 4),
        sievetools.Sieve(6, 5),
        sievetools.Sieve(10, 0),
        sievetools.Sieve(10, 1),
        sievetools.Sieve(10, 2),
        ]


def test_sievetools_CompoundSieve_from_boolean_patterns_03():
    r'''From no boolean patterns.
    '''

    compound_sieve = sievetools.CompoundSieve.from_boolean_patterns([])
    assert compound_sieve.sieves == []