from abjad import *
from abjad.tools import sequencetools


def test_seqtools_CyclicMatrix_columns_01():

    cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert cyclic_matrix.columns == ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert cyclic_matrix.columns[2] == (2, 12, 22)
    assert cyclic_matrix.columns[2][0] == 2


def test_seqtools_CyclicMatrix_columns_02():

    cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert cyclic_matrix.columns == ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert cyclic_matrix.columns[99] == (3, 13, 23)
    assert cyclic_matrix.columns[99][99] == 3
