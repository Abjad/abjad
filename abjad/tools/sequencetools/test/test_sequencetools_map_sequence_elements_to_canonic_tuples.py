# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_map_sequence_elements_to_canonic_tuples_01():

    sequence_1 = range(10)
    sequence_2 = sequencetools.map_sequence_elements_to_canonic_tuples(sequence_1)

    assert sequence_2 == [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]


def test_sequencetools_map_sequence_elements_to_canonic_tuples_02():

    sequence_1 = range(10)
    false = sequencetools.map_sequence_elements_to_canonic_tuples(
        sequence_1, decrease_parts_monotonically=False)

    assert false == [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]


def test_sequencetools_map_sequence_elements_to_canonic_tuples_03():
    r'''Raise TypeError when sequence_1 is not a list.
    Raise ValueError on noninteger elements in sequence_1.
    '''

    statement = "sequencetools.map_sequence_elements_to_canonic_tuples('foo')"
    assert pytest.raises(TypeError, statement)
    statement = 'sequencetools.map_sequence_elements_to_canonic_tuples(' + \
        '[Fraction(1, 2), Fraction(1, 2)])'
    assert pytest.raises(ValueError, statement)
