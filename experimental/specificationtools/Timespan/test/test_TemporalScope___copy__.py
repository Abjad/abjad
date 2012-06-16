from experimental import specificationtools
from fractions import Fraction
import copy


def test_Timespan___copy___01():

    start = specificationtools.TemporalCursor(edge=Right, multiplier=Fraction(1, 3))
    stop = specificationtools.TemporalCursor(edge=Right, multiplier=Fraction(2, 3))
    scope_1 = specificationtools.Timespan(start=start, stop=stop)
    scope_2 = copy.deepcopy(scope_1)

    assert isinstance(scope_1, specificationtools.Timespan)
    assert isinstance(scope_2, specificationtools.Timespan)
    assert not scope_1 is scope_2
    assert scope_1 == scope_2
