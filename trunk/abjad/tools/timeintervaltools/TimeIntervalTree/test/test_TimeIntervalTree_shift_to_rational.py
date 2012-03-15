from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree


def test_TimeIntervalTree_shift_to_rational_01():

    t1 = TimeInterval(-1, 3)
    t2 = TimeInterval(0, 1)
    t3 = TimeInterval(1, 2)

    tree = TimeIntervalTree([t1, t2, t3])
    offset = Offset(10, 1)
    result = tree.shift_to_rational(offset)

    assert type(result) == type(tree)
    assert result.duration == tree.duration
    assert [x.signature for x in result] == [ 
        (Offset(10, 1), Offset(14, 1)),
        (Offset(11, 1), Offset(12, 1)),
        (Offset(12, 1), Offset(13, 1))]

