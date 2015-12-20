# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmmakertools_CompoundSieve_01():
    r'''Boolean operator defaults to OR.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 0), rhythmmakertools.Sieve(3, 0)])

    assert sieve.logical_operator == 'or'


def test_rhythmmakertools_CompoundSieve_02():
    r'''Logical OR.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 0), rhythmmakertools.Sieve(3, 0)])

    assert sieve.boolean_train == [1, 0, 1, 1, 1, 0]
    assert sieve.indices == [0, 2, 3, 4]


def test_rhythmmakertools_CompoundSieve_03():
    r'''Logical OR.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 1), rhythmmakertools.Sieve(3, 0)])

    assert sieve.boolean_train == [1, 1, 0, 1, 0, 1]
    assert sieve.indices == [0, 1, 3, 5]


def test_rhythmmakertools_CompoundSieve_04():
    r'''Logical AND.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 0), rhythmmakertools.Sieve(3, 0)], 'and')

    assert sieve.logical_operator == 'and'
    assert sieve.boolean_train == [1, 0, 0, 0, 0, 0]
    assert sieve.indices == [0]


def test_rhythmmakertools_CompoundSieve_05():
    r'''Logical AND.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 1), rhythmmakertools.Sieve(3, 0)], 'and')

    assert sieve.boolean_train == [0, 0, 0, 1, 0, 0]
    assert sieve.indices == [3]


def test_rhythmmakertools_CompoundSieve_06():
    r'''Logical XOR.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 0), rhythmmakertools.Sieve(3, 0)], 'xor')

    assert sieve.logical_operator == 'xor'
    assert sieve.boolean_train == [0, 0, 1, 1, 1, 0]
    assert sieve.indices == [2, 3, 4]


def test_rhythmmakertools_CompoundSieve_07():
    r'''Logical XOR.
    '''

    sieve = rhythmmakertools.CompoundSieve([rhythmmakertools.Sieve(2, 1), rhythmmakertools.Sieve(3, 0)], 'xor')

    assert sieve.boolean_train == [1, 1, 0, 0, 0, 1]
    assert sieve.indices == [0, 1, 5]