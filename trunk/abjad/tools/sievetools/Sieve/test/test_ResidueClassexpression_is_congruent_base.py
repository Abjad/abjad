from abjad import *
from abjad.tools import sievetools


def test_ResidueClassexpression_is_congruent_base_01():
    '''Works with negative integers.'''

    sieve = sievetools.cycle_tokens_to_sieve((5, [0, 1]), (6, [0]))

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


def test_ResidueClassexpression_is_congruent_base_02():
    '''Works with zero.'''

    sieve = sievetools.cycle_tokens_to_sieve((5, [0, 1]), (6, [0]))

    "{RC(5, 0) | RC(5, 1) | RC(6, 0)}"

    assert sieve.is_congruent_base(0)


def test_ResidueClassexpression_is_congruent_base_03():
    '''Works with positive integers.'''

    sieve = sievetools.cycle_tokens_to_sieve((5, [0, 1]), (6, [0]))

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
