from experimental import specificationtools
from fractions import Fraction
import copy


def test_TemporalScope___copy___01():

    start = specificationtools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
    stop = specificationtools.Timepoint(edge=Right, multiplier=Fraction(2, 3))
    timespan_1 = specificationtools.Timespan(start=start, stop=stop)
    timespan_2 = copy.deepcopy(timespan_1)

    assert isinstance(timespan_1, specificationtools.Timespan)
    assert isinstance(timespan_2, specificationtools.Timespan)
    assert not timespan_1 is timespan_2
    assert timespan_1 == timespan_2
