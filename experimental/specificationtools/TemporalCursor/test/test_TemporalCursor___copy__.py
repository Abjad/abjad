from experimental import specificationtools
from fractions import Fraction
import copy


def test_TemporalCursor___copy___01():

    cursor_1 = specificationtools.TemporalCursor(edge=Right, multiplier=Fraction(1, 3))
    cursor_2 = copy.deepcopy(cursor_1)

    assert isinstance(cursor_1, specificationtools.TemporalCursor)
    assert isinstance(cursor_2, specificationtools.TemporalCursor)
    assert not cursor_1 is cursor_2
    assert cursor_1 == cursor_2
