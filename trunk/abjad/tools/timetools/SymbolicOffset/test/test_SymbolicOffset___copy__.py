import copy
import fractions
from experimental import *


def test_SymbolicOffset___copy___01():

    offset_1 = timetools.SymbolicOffset(edge=Right, multiplier=fractions.Fraction(1, 3))
    offset_2 = copy.deepcopy(offset_1)

    assert isinstance(offset_1, timetools.SymbolicOffset)
    assert isinstance(offset_2, timetools.SymbolicOffset)
    assert not offset_1 is offset_2
    assert offset_1 == offset_2
