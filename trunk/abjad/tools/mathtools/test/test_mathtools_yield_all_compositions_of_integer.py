from abjad import *
from abjad.tools import mathtools


def test_mathtools_yield_all_compositions_of_integer_01():
    '''Yield all compositions (that is, ordered partitions)
    of positive integer n, in descending lex order.'''


    compositions = mathtools.yield_all_compositions_of_integer(5)
    compositions = list(compositions)

    assert compositions[0] == (5,)
    assert compositions[1] == (4, 1)
    assert compositions[2] == (3, 2)
    assert compositions[3] == (3, 1, 1)
    assert compositions[4] == (2, 3)
    assert compositions[5] == (2, 2, 1)
    assert compositions[6] == (2, 1, 2)
    assert compositions[7] == (2, 1, 1, 1)
    assert compositions[8] == (1, 4)
    assert compositions[9] == (1, 3, 1)
    assert compositions[10] == (1, 2, 2)
    assert compositions[11] == (1, 2, 1, 1)
    assert compositions[12] == (1, 1, 3)
    assert compositions[13] == (1, 1, 2, 1)
    assert compositions[14] == (1, 1, 1, 2)
    assert compositions[15] == (1, 1, 1, 1, 1)
