from abjad import *
from abjad.tools import seqtools


def test_seqtools_Matrix_rows_01( ):

    matrix = seqtools.Matrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix.rows[2] == (20, 21, 22, 23)
    assert matrix.rows[2][0] == 20
