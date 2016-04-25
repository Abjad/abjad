# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicMatrix_rows_01():

    cyclic_matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert cyclic_matrix.rows == \
        ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.rows[2] == (20, 21, 22, 23)
    assert cyclic_matrix.rows[2][0] == 20


def test_datastructuretools_CyclicMatrix_rows_02():

    cyclic_matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert cyclic_matrix.rows == \
        ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.rows[99] == (0, 1, 2, 3)
    assert cyclic_matrix.rows[99][99] == 3
