from experimental import specificationtools
from experimental import timespaninequalitytools
from fractions import Fraction
import copy


def test_SingleSourceTimespan___copy___01():

    timespan_1 = timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
    timespan_2 = copy.deepcopy(timespan_1)

    assert isinstance(timespan_1, timespantools.SingleSourceTimespan)
    assert isinstance(timespan_2, timespantools.SingleSourceTimespan)
    assert not timespan_1 is timespan_2
    assert timespan_1 == timespan_2
