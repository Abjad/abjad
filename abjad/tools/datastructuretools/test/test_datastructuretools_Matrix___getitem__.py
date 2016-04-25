# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Matrix___getitem___01():

    matrix = datastructuretools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix[:] == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix[2] == (20, 21, 22, 23)
    assert matrix[2][0] == 20
