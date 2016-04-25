# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicMatrix_columns_01():

    cyclic_matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert cyclic_matrix.columns == \
        ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert cyclic_matrix.columns[2] == (2, 12, 22)
    assert cyclic_matrix.columns[2][0] == 2


def test_datastructuretools_CyclicMatrix_columns_02():

    cyclic_matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert cyclic_matrix.columns == \
        ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert cyclic_matrix.columns[99] == (3, 13, 23)
    assert cyclic_matrix.columns[99][99] == 3
