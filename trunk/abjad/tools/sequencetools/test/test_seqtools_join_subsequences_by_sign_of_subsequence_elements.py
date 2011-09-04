from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_join_subsequences_by_sign_of_subsequence_elements_01():

    l = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
    t = sequencetools.join_subsequences_by_sign_of_subsequence_elements(l)

    assert t == [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]


def test_sequencetools_join_subsequences_by_sign_of_subsequence_elements_02():

    l = [[1, 2], [], [], [3, 4, 5], [6, 7]]
    t = sequencetools.join_subsequences_by_sign_of_subsequence_elements(l)

    assert t == [[1, 2], [], [3, 4, 5, 6, 7]]
