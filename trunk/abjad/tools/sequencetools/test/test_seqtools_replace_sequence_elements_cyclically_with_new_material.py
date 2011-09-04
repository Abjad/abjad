from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_01():
    '''Overwrite elements in l at cyclic indices with cyclic material.
    Here replace at every index equal to 0 % 2 and read ['A', 'B'] % 3.'''

    l = range(20)
    indices = ([0], 2)
    material = (['A', 'B'], 3)

    t = sequencetools.replace_sequence_elements_cyclically_with_new_material(l, indices, material)

    assert t == ['A', 1, 'B', 3, 4, 5,
        'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15, 16, 17, 'A', 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_02():
    '''Overwrite elements in l at cyclic indices with cyclic material.
    Here replace at indices equal to 0 % 2 and read ['*'] % 1.'''

    l = range(20)
    indices = ([0], 2)
    material = (['*'], 1)

    t = sequencetools.replace_sequence_elements_cyclically_with_new_material(l, indices, material)

    assert t == ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15, '*', 17, '*', 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_03():
    '''Overwrite elements in l at cyclic indices with cyclic material.
    Here replace at indices equal to 0 % 2 and read material only once.'''

    l = range(20)
    indices = ([0], 2)
    material = (['A', 'B', 'C', 'D'], None)

    t = sequencetools.replace_sequence_elements_cyclically_with_new_material(l, indices, material)

    assert t == ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_04():
    '''Overwrite elements in l at cyclic indices with cyclic material.
    Here replace at indices 0, 1, 8, 13 only and read material only once.'''

    l = range(20)
    indices = ([0, 1, 8, 13], None)
    material = (['A', 'B', 'C', 'D'], None)

    t = sequencetools.replace_sequence_elements_cyclically_with_new_material(l, indices, material)

    assert t == ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15, 16, 17, 18, 19]


def test_sequencetools_replace_sequence_elements_cyclically_with_new_material_05():
    '''Raise TypeError when l is not a list.'''

    assert py.test.raises(TypeError,
        "sequencetools.replace_sequence_elements_cyclically_with_new_material('foo', ([0], 2), ([10, 12], 3))")
