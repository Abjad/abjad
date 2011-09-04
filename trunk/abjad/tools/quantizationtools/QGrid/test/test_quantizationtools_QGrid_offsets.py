from abjad.tools.durationtools import Offset
from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_offsets_01():

    assert QGrid([0], 0).offsets == (
        Offset(0), Offset(1)
    )

    assert QGrid([0, 0], 0).offsets == (
        Offset(0), Offset(1, 2), Offset(1)
    )

    assert QGrid([0, [[[1, 2], 3], 4], 5], 6).offsets == (
        Offset(0, 1), Offset(1, 3), Offset(3, 8), Offset(5, 12),
        Offset(1, 2), Offset(2, 3), Offset(1, 1)
    )
