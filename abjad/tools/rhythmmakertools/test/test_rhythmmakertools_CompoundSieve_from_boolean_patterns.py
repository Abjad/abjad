# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_CompoundSieve_from_boolean_patterns_01():
    r'''From one boolean pattern.
    '''

    pattern = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    compound_sieve = rhythmmakertools.CompoundSieve.from_boolean_patterns([pattern])

    assert compound_sieve.sieves == [
        rhythmmakertools.Sieve(6, 0),
        rhythmmakertools.Sieve(6, 4),
        rhythmmakertools.Sieve(6, 5),
        ]


def test_rhythmmakertools_CompoundSieve_from_boolean_patterns_02():
    r'''From multiple boolean patterns.
    '''

    pattern_1 = rhythmmakertools.BooleanPattern(indices=[0, 4, 5], period=6)
    pattern_2 = rhythmmakertools.BooleanPattern(indices=[0, 1, 2], period=10)
    patterns = [pattern_1, pattern_2]
    compound_sieve = rhythmmakertools.CompoundSieve.from_boolean_patterns(patterns)

    assert compound_sieve.sieves == [
        rhythmmakertools.Sieve(6, 0),
        rhythmmakertools.Sieve(6, 4),
        rhythmmakertools.Sieve(6, 5),
        rhythmmakertools.Sieve(10, 0),
        rhythmmakertools.Sieve(10, 1),
        rhythmmakertools.Sieve(10, 2),
        ]


def test_rhythmmakertools_CompoundSieve_from_boolean_patterns_03():
    r'''From no boolean patterns.
    '''

    compound_sieve = rhythmmakertools.CompoundSieve.from_boolean_patterns([])
    assert compound_sieve.sieves == []