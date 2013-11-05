# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_sequencetools_repeat_sequence_elements_n_times_each_01():

    sequence_1 = [1, 1, 2, 3, 5, 5, 6]
    sequence_2 = sequencetools.repeat_sequence_elements_n_times_each(sequence_1, 2)

    assert sequence_2 == [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]


def test_sequencetools_repeat_sequence_elements_n_times_each_02():

    sequence_1 = [1, -1, 2, -3, 5, -5, 6]
    sequence_2 = sequencetools.repeat_sequence_elements_n_times_each(sequence_1, 2)

    assert sequence_2 == [1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6]


def test_sequencetools_repeat_sequence_elements_n_times_each_03():

    assert pytest.raises(
        TypeError, "sequencetools.repeat_sequence_elements_n_times_each('foo')")
