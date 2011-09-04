from abjad import *
from abjad.tools import sequencetools


def test_seqtools_CyclicMatrix_rows_01():

    cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert cyclic_matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.rows[2] == (20, 21, 22, 23)
    assert cyclic_matrix.rows[2][0] == 20


def test_seqtools_CyclicMatrix_rows_02():

    cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert cyclic_matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.rows[99] == (0, 1, 2, 3)
    assert cyclic_matrix.rows[99][99] == 3
