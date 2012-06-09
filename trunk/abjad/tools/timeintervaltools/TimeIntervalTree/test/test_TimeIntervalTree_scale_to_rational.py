from fractions import Fraction
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree


def test_TimeIntervalTree_scale_to_rational_01():
    t1 = TimeInterval(0, 4)
    t2 = TimeInterval(1, 8)
    t3 = TimeInterval(2, 6)

    tree = TimeIntervalTree([t1, t2, t3])
    scalar = Fraction(1, 4)
    result = tree.scale_to_rational(scalar)

    assert type(result) == type(tree)
    assert [x.signature for x in result] == [
        (Offset(0, 1), Offset(1, 8)),
        (Offset(1, 32), Offset(1, 4)),
        (Offset(1, 16), Offset(3, 16))]
    assert result.duration == scalar
    
