from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_map_sequence_elements_to_canonic_tuples_01():

    l = range(10)
    t = sequencetools.map_sequence_elements_to_canonic_tuples(l)

    assert t == [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]


def test_sequencetools_map_sequence_elements_to_canonic_tuples_02():

    l = range(10)
    t = sequencetools.map_sequence_elements_to_canonic_tuples(
        l, direction = 'little-endian')

    assert t == [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]


def test_sequencetools_map_sequence_elements_to_canonic_tuples_03():
    '''Raise TypeError when l is not a list.
        Raise ValueError on noninteger elements in l.'''

    assert py.test.raises(
        TypeError, "sequencetools.map_sequence_elements_to_canonic_tuples('foo')")
    assert py.test.raises(ValueError,
        'sequencetools.map_sequence_elements_to_canonic_tuples('
        '[Fraction(1, 2), Fraction(1, 2)])')
