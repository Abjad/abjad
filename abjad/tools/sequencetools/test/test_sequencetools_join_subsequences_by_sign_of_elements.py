# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_join_subsequences_by_sign_of_elements_01():

    sequence_1 = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
    sequence_2 = sequencetools.join_subsequences_by_sign_of_elements(sequence_1)

    assert sequence_2 == [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]


def test_sequencetools_join_subsequences_by_sign_of_elements_02():

    sequence_1 = [[1, 2], [], [], [3, 4, 5], [6, 7]]
    sequence_2 = sequencetools.join_subsequences_by_sign_of_elements(sequence_1)

    assert sequence_2 == [[1, 2], [], [3, 4, 5, 6, 7]]
