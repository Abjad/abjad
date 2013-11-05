# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_sequencetools_negate_absolute_value_of_sequence_elements_at_indices_01():

    sequence_1 = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
    sequence_2 = sequencetools.negate_absolute_value_of_sequence_elements_at_indices(sequence_1, [0, 1, 2])

    assert sequence_2 == [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]


def test_sequencetools_negate_absolute_value_of_sequence_elements_at_indices_02():

    assert pytest.raises(TypeError,
        "sequencetools.negate_absolute_value_of_sequence_elements_at_indices('foo', [0, 1, 2])")
