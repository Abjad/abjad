from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_repeat_sequence_to_length_01():
    '''Repeat list to length.'''

    assert sequencetools.repeat_sequence_to_length(range(5), 11) == [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]


def test_sequencetools_repeat_sequence_to_length_02():
    '''Repeat list to length.'''

    t = sequencetools.repeat_sequence_to_length([0, -1, -2, -3, -4], 11)
    assert t == [0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0]


def test_sequencetools_repeat_sequence_to_length_03():
    '''When length is less than length of list
    return only the first length elements of list.
    '''

    t = sequencetools.repeat_sequence_to_length(range(5), 3)
    assert t == [0, 1, 2]


def test_sequencetools_repeat_sequence_to_length_04():
    '''When length is zero, return an empty list.'''

    t = sequencetools.repeat_sequence_to_length(range(5), 0)
    assert t == []


def test_sequencetools_repeat_sequence_to_length_05():
    '''List must not be empty.'''

    assert py.test.raises(ValueError, 'sequencetools.repeat_sequence_to_length([], 2)')


def test_sequencetools_repeat_sequence_to_length_06():
    '''Optional start index less than length of list.'''

    t = sequencetools.repeat_sequence_to_length([1, 2, 3], 10, 2)

    assert t == [3, 1, 2, 3, 1, 2, 3, 1, 2, 3]


def test_sequencetools_repeat_sequence_to_length_07():
    '''Optional start index greater than length of list is OK.'''

    t = sequencetools.repeat_sequence_to_length([1, 2, 3], 10, 100)

    assert t == [2, 3, 1, 2, 3, 1, 2, 3, 1, 2]


def test_sequencetools_repeat_sequence_to_length_08():
    '''Repeat Abjad container to length.
    '''

    container = Container("c'8 d'8 e'8")
    new = sequencetools.repeat_sequence_to_length(container, 5)
    assert new.format == Container("c'8 d'8 e'8 c'8 d'8").format
    assert new[0] is not container[0]
