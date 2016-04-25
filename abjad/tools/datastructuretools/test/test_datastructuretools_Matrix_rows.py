# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Matrix_rows_01():

    matrix = datastructuretools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix.rows[2] == (20, 21, 22, 23)
    assert matrix.rows[2][0] == 20
