# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_retain_elements_at_indices_01():

    sequence_2 = sequencetools.retain_elements_at_indices(range(20), [1, 16, 17, 18])
    assert sequence_2 == [1, 16, 17, 18]


def test_sequencetools_retain_elements_at_indices_02():

    sequence_2 = sequencetools.retain_elements_at_indices(range(20), [])
    assert sequence_2 == []


def test_sequencetools_retain_elements_at_indices_03():

    sequence_2 = sequencetools.retain_elements_at_indices(range(20), [99, 100, 101])
    assert sequence_2 == []
