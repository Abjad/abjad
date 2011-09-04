from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_get_sequence_element_at_cyclic_index_01():
    '''Get element at nonnegative cyclic index.
    '''

    iterable = 'string'

    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 0) == 's'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 1) == 't'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 2) == 'r'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 3) == 'i'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 4) == 'n'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 5) == 'g'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 6) == 's'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 7) == 't'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 8) == 'r'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, 9) == 'i'


def test_sequencetools_get_sequence_element_at_cyclic_index_02():
    '''Get element at negative cyclic index.
    '''

    iterable = 'string'

    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -1) == 'g'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -2) == 'n'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -3) == 'i'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -4) == 'r'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -5) == 't'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -6) == 's'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -7) == 'g'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -8) == 'n'
    assert sequencetools.get_sequence_element_at_cyclic_index(iterable, -9) == 'i'
