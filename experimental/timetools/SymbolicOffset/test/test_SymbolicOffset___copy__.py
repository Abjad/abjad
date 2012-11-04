import copy
import fractions
from experimental import *


def test_SymbolicOffset___copy___01():

    timepoint_1 = timetools.SymbolicOffset(edge=Right, multiplier=fractions.Fraction(1, 3))
    timepoint_2 = copy.deepcopy(timepoint_1)

    assert isinstance(timepoint_1, timetools.SymbolicOffset)
    assert isinstance(timepoint_2, timetools.SymbolicOffset)
    assert not timepoint_1 is timepoint_2
    assert timepoint_1 == timepoint_2
