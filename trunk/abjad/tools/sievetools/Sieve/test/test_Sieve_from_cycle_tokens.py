# -*- encoding: utf-8 -*-
from abjad import *


def test_Sieve_from_cycle_tokens_01():
    r'''Single length-2 cycle token with modulo and residue list.
    '''

    cycle_token = (6, [0, 4, 5])
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token)
    RC = sievetools.ResidueClass

    assert sieve.rcs == [RC(6, 0), RC(6, 4), RC(6, 5)]


def test_Sieve_from_cycle_tokens_02():
    r'''Single length-3 cycle token with modulo, residue list and offset.
    '''

    cycle_token = (6, [0, 4, 5], 1)
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token)
    RC = sievetools.ResidueClass

    assert sieve.rcs == [RC(6, 0), RC(6, 1), RC(6, 5)]


def test_Sieve_from_cycle_tokens_03():
    r'''Large offset.
    '''

    cycle_token = (6, [0, 4, 5], 99)
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token)
    RC = sievetools.ResidueClass

    assert sieve.rcs == [RC(6, 1), RC(6, 2), RC(6, 3)]


def test_Sieve_from_cycle_tokens_04():
    r'''Unsorted residues are sorted on initialization.
    '''

    cycle_token = (6, [5, 0, 4])
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token)
    RC = sievetools.ResidueClass

    assert sieve.rcs == [RC(6, 0), RC(6, 4), RC(6, 5)]

def test_Sieve_from_cycle_tokens_05():
    r'''Arbitrarily many cycle tokens.
    '''

    cycle_token_1 = (6, [0, 4, 5])
    cycle_token_2 = (10, [0, 1, 2])
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token_1, cycle_token_2)

    "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 0) | RC(10, 1) | RC(10, 2)}"

    RC = sievetools.ResidueClass
    assert sieve.rcs == [
        RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 0), RC(10, 1), RC(10, 2)]


def test_Sieve_from_cycle_tokens_06():
    r'''Unsorted RCs are sorted on initialization.
    '''

    cycle_token_1 = (6, [0, 4, 5])
    cycle_token_2 = (10, [0, 1, 2])
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token_2, cycle_token_1)

    "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 0) | RC(10, 1) | RC(10, 2)}"

    RC = sievetools.ResidueClass
    assert sieve.rcs == [
        RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 0), RC(10, 1), RC(10, 2)]


def test_Sieve_from_cycle_tokens_07():
    r'''Cycle tokens allow optional offset values.
    '''

    cycle_token_1 = (6, [0, 4, 5])
    cycle_token_2 = (10, [0, 1, 2], 6)
    sieve = sievetools.Sieve.from_cycle_tokens(cycle_token_2, cycle_token_1)

    "{RC(6, 0) | RC(6, 4) | RC(6, 5) | RC(10, 6) | RC(10, 7) | RC(10, 8)}"

    RC = sievetools.ResidueClass
    assert sieve.rcs == [
        RC(6, 0), RC(6, 4), RC(6, 5), RC(10, 6), RC(10, 7), RC(10, 8)]


def test_Sieve_from_cycle_tokens_08():
    r'''Works with no cycle tokens.
    '''

    sieve = sievetools.Sieve.from_cycle_tokens()
    assert sieve.rcs == []


def test_Sieve_from_cycle_tokens_09():
    r'''Sieves count as cycle tokens in themselves.
    '''

    RC = sievetools.ResidueClass
    sieve_cycle_token = RC(6, 0) | RC(6, 1)
    sieve = sievetools.Sieve.from_cycle_tokens(sieve_cycle_token)

    assert sieve.rcs == [RC(6, 0), RC(6, 1)]
