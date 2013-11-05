# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_01():
    r'''Overwrite elements in sequence_1 at cyclic indices with cyclic material.
    Here replace at every index equal to 0 % 2 and read ['A', 'B'] % 3.'''

    sequence_1 = range(20)
    indices = ([0], 2)
    material = (['A', 'B'], 3)

    a = sequencetools.replace_sequence_elements_cyclically_with_new_material(sequence_1, indices, material)

    assert a == ['A', 1, 'B', 3, 4, 5,
        'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15, 16, 17, 'A', 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_02():
    r'''Overwrite elements in sequence_1 at cyclic indices with cyclic material.
    Here replace at indices equal to 0 % 2 and read ['*'] % 1.'''

    sequence_1 = range(20)
    indices = ([0], 2)
    material = (['*'], 1)

    sequence_2 = sequencetools.replace_sequence_elements_cyclically_with_new_material(sequence_1, indices, material)

    assert sequence_2 == ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15, '*', 17, '*', 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_03():
    r'''Overwrite elements in sequence_1 at cyclic indices with cyclic material.
    Here replace at indices equal to 0 % 2 and read material only once.'''

    sequence_1 = range(20)
    indices = ([0], 2)
    material = (['A', 'B', 'C', 'D'], None)

    overwrite = sequencetools.replace_sequence_elements_cyclically_with_new_material(sequence_1, indices, material)

    assert overwrite == ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_04():
    r'''Overwrite elements in sequence_1 at cyclic indices with cyclic material.
    Here replace at indices 0, 1, 8, 13 only and read material only once.'''

    sequence_1 = range(20)
    indices = ([0, 1, 8, 13], None)
    material = (['A', 'B', 'C', 'D'], None)

    a = sequencetools.replace_sequence_elements_cyclically_with_new_material(sequence_1, indices, material)

    assert a == ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15, 16, 17, 18, 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_05():
    r'''Raise TypeError when sequence_1 is not a list.
    '''

    assert py.test.raises(TypeError,
        "sequencetools.replace_sequence_elements_cyclically_with_new_material('foo', ([0], 2), ([10, 12], 3))")
