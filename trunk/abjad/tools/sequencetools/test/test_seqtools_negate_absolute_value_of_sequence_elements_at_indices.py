from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_negate_absolute_value_of_sequence_elements_at_indices_01():

    l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
    t = sequencetools.negate_absolute_value_of_sequence_elements_at_indices(l, [0, 1, 2])

    assert t == [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]


def test_sequencetools_negate_absolute_value_of_sequence_elements_at_indices_02():

    assert py.test.raises(TypeError,
        "sequencetools.negate_absolute_value_of_sequence_elements_at_indices('foo', [0, 1, 2])")
