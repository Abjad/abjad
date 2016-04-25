# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Matrix_columns_01():

    matrix = datastructuretools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix.columns == \
        ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert matrix.columns[2] == (2, 12, 22)
    assert matrix.columns[2][0] == 2
