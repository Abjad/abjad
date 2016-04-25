# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_overwrite_elements_01():

    sequence_1 = range(10)
    sequence_2 = sequencetools.overwrite_elements(sequence_1, [(0, 3), (5, 3)])

    assert sequence_2 == [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]


def test_sequencetools_overwrite_elements_02():

    sequence_1 = range(10)
    sequence_2 = sequencetools.overwrite_elements(sequence_1, [(0, 99)])

    assert sequence_2 == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
