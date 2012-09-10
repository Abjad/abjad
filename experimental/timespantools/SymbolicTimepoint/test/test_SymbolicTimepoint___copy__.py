import copy
import fractions
from experimental import *


def test_SymbolicTimepoint___copy___01():

    timepoint_1 = timespantools.SymbolicTimepoint(edge=Right, multiplier=fractions.Fraction(1, 3))
    timepoint_2 = copy.deepcopy(timepoint_1)

    assert isinstance(timepoint_1, timespantools.SymbolicTimepoint)
    assert isinstance(timepoint_2, timespantools.SymbolicTimepoint)
    assert not timepoint_1 is timepoint_2
    assert timepoint_1 == timepoint_2
