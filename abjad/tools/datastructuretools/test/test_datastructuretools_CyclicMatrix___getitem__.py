# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicMatrix___getitem___01():

    matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix[2] == (20, 21, 22, 23)
    assert matrix[2][0] == 20


def test_datastructuretools_CyclicMatrix___getitem___02():

    matrix = datastructuretools.CyclicMatrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix[99] == (0, 1, 2, 3)
    assert matrix[99][99] == 3
