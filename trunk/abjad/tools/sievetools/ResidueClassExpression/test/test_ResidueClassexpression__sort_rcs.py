from abjad import *
from abjad.tools import sievetools


def test_ResidueClassexpression__sort_rcs_01():
    '''Unsorted RCs are sorted on RC expression initialization.'''

    RC = sievetools.ResidueClass
    rcexpression = sievetools.ResidueClassExpression([RC(10, 0), RC(9, 0), RC(8, 0)])
    assert rcexpression.rcs == [RC(8, 0), RC(9, 0), RC(10, 0)]


def test_ResidueClassexpression__sort_rcs_02():
    '''Unsorted RCs are sorted on RC expression initialization.'''

    RC = sievetools.ResidueClass
    rcexpression = sievetools.ResidueClassExpression([RC(8, 7), RC(8, 1), RC(8, 2)])
    assert rcexpression.rcs == [RC(8, 1), RC(8, 2), RC(8, 7)]
