from experimental import specificationtools
from fractions import Fraction
import copy


def test_TemporalScope___copy___01():

    start = specificationtools.TemporalCursor(edge=right, multiplier=Fraction(1, 3))
    stop = specificationtools.TemporalCursor(edge=right, multiplier=Fraction(2, 3))
    scope_1 = specificationtools.TemporalScope(start=start, stop=stop)
    scope_2 = copy.deepcopy(scope_1)

    assert isinstance(scope_1, specificationtools.TemporalScope)
    assert isinstance(scope_2, specificationtools.TemporalScope)
    assert not scope_1 is scope_2
    assert scope_1 == scope_2
