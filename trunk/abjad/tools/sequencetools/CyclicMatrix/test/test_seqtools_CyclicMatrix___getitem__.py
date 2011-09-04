from abjad import *
from abjad.tools import sequencetools


def test_seqtools_CyclicMatrix___getitem___01():

    matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert matrix[2] == (20, 21, 22, 23)
    assert matrix[2][0] == 20


def test_seqtools_CyclicMatrix___getitem___02():

    matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    assert matrix[99] == (0, 1, 2, 3)
    assert matrix[99][99] == 3
