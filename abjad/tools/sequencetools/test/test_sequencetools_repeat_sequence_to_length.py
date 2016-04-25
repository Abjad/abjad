# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_repeat_sequence_to_length_01():
    r'''Repeat list to length.
    '''

    assert sequencetools.repeat_sequence_to_length(list(range(5)), 11) == [
        0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]


def test_sequencetools_repeat_sequence_to_length_02():
    r'''Repeat list to length.
    '''

    sequence_2 = sequencetools.repeat_sequence_to_length(
        [0, -1, -2, -3, -4], 11)
    assert sequence_2 == [0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0]


def test_sequencetools_repeat_sequence_to_length_03():
    r'''When length is less than length of list
    return only the first length elements of list.
    '''

    when = sequencetools.repeat_sequence_to_length(list(range(5)), 3)
    assert when == [0, 1, 2]


def test_sequencetools_repeat_sequence_to_length_04():
    r'''When length is zero, return an empty list.
    '''

    sequence_2 = sequencetools.repeat_sequence_to_length(list(range(5)), 0)
    assert sequence_2 == []


def test_sequencetools_repeat_sequence_to_length_05():
    r'''List must not be empty.
    '''

    statement = 'sequencetools.repeat_sequence_to_length([], 2)'
    assert pytest.raises(ValueError, statement)


def test_sequencetools_repeat_sequence_to_length_06():
    r'''Optional start index less than length of list.
    '''

    sequence_2 = sequencetools.repeat_sequence_to_length([1, 2, 3], 10, 2)

    assert sequence_2 == [3, 1, 2, 3, 1, 2, 3, 1, 2, 3]


def test_sequencetools_repeat_sequence_to_length_07():
    r'''Optional start index greater than length of list is OK.
    '''

    sequence_2 = sequencetools.repeat_sequence_to_length([1, 2, 3], 10, 100)

    assert sequence_2 == [2, 3, 1, 2, 3, 1, 2, 3, 1, 2]
