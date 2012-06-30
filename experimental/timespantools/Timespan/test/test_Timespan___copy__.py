from experimental import specificationtools
from experimental import timespantools
from fractions import Fraction
import copy


def test_Timespan___copy___01():

    start = specificationtools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
    stop = specificationtools.Timepoint(edge=Right, multiplier=Fraction(2, 3))
    timespan_1 = timespantools.Timespan(start=start, stop=stop)
    timespan_2 = copy.deepcopy(timespan_1)

    assert isinstance(timespan_1, timespantools.Timespan)
    assert isinstance(timespan_2, timespantools.Timespan)
    assert not timespan_1 is timespan_2
    assert timespan_1 == timespan_2
