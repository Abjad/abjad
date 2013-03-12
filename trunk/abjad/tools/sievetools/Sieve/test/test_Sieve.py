from abjad.tools import sievetools
from abjad.tools.sievetools import ResidueClass as RC
import py.test


def test_Sieve_01():
    '''Boolean operator defaults to OR.
    '''

    t = sievetools.Sieve([RC(2, 0), RC(3, 0)])

    assert t.logical_operator == 'or'


def test_Sieve_02():
    '''Logical OR.
    '''

    t = sievetools.Sieve([RC(2, 0), RC(3, 0)])

    assert t.get_boolean_train(6) == [1, 0, 1, 1, 1, 0]
    assert t.get_congruent_bases(6) == [0, 2, 3, 4, 6]


def test_Sieve_03():
    '''Logical OR.
    '''

    t = sievetools.Sieve([RC(2, 1), RC(3, 0)])

    assert t.get_boolean_train(6) == [1, 1, 0, 1, 0, 1]
    assert t.get_congruent_bases(6) == [0, 1, 3, 5, 6]


def test_Sieve_04():
    '''Logical AND.
    '''

    t = sievetools.Sieve([RC(2, 0), RC(3, 0)], 'and')

    assert t.logical_operator == 'and'
    assert t.get_boolean_train(6) == [1, 0, 0, 0, 0, 0]
    assert t.get_congruent_bases(6) == [0, 6]


def test_Sieve_05():
    '''Logical AND.
    '''

    t = sievetools.Sieve([RC(2, 1), RC(3, 0)], 'and')

    assert t.get_boolean_train(6) == [0, 0, 0, 1, 0, 0]
    assert t.get_congruent_bases(6) == [3]


def test_Sieve_06():
    '''Logical XOR.
    '''

    t = sievetools.Sieve([RC(2, 0), RC(3, 0)], 'xor')

    assert t.logical_operator == 'xor'
    assert t.get_boolean_train(6) == [0, 0, 1, 1, 1, 0]
    assert t.get_congruent_bases(6) == [2, 3, 4]


def test_Sieve_07():
    '''Logical XOR.
    '''

    t = sievetools.Sieve([RC(2, 1), RC(3, 0)], 'xor')

    assert t.get_boolean_train(6) == [1, 1, 0, 0, 0, 1]
    assert t.get_congruent_bases(6) == [0, 1, 5, 6]
