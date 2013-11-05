# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sievetools


def test_sievetools_Sieve_is_congruent_base_01():
    r'''Works with negative integers.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens((5, [0, 1]), (6, [0]))


    "{RC(5, 0) | RC(5, 1) | RC(6, 0)}"

    assert sieve.is_congruent_base(-10)
    assert sieve.is_congruent_base(-9)
    assert not sieve.is_congruent_base(-8)
    assert sieve.is_congruent_base(-6)
    assert sieve.is_congruent_base(-5)
    assert sieve.is_congruent_base(-4)
    assert not sieve.is_congruent_base(-3)
    assert not sieve.is_congruent_base(-2)
    assert not sieve.is_congruent_base(-1)


def test_sievetools_Sieve_is_congruent_base_02():
    r'''Works with zero.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens((5, [0, 1]), (6, [0]))

    "{RC(5, 0) | RC(5, 1) | RC(6, 0)}"

    assert sieve.is_congruent_base(0)


def test_sievetools_Sieve_is_congruent_base_03():
    r'''Works with positive integers.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens((5, [0, 1]), (6, [0]))

    "{RC(5, 0) | RC(5, 1) | RC(6, 0)}"

    assert sieve.is_congruent_base(1)
    assert not sieve.is_congruent_base(2)
    assert not sieve.is_congruent_base(3)
    assert not sieve.is_congruent_base(4)
    assert sieve.is_congruent_base(5)
    assert sieve.is_congruent_base(6)
    assert not sieve.is_congruent_base(7)
    assert not sieve.is_congruent_base(8)
    assert not sieve.is_congruent_base(9)
    assert sieve.is_congruent_base(10)
