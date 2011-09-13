from abjad import *


def test_pitchtools_TwelveToneRow_transpose_01():

    row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
    assert row.transpose(0) == row

    new = pitchtools.TwelveToneRow([11, 1, 3, 7, 9, 8, 6, 4, 2, 10, 5, 0])
    assert row.transpose(1) == new

    new = pitchtools.TwelveToneRow([0, 2, 4, 8, 10, 9, 7, 5, 3, 11, 6, 1])
    assert row.transpose(2) == new

    new = pitchtools.TwelveToneRow([1, 3, 5, 9, 11, 10, 8, 6, 4, 0, 7, 2])
    assert row.transpose(3) == new

    new = pitchtools.TwelveToneRow([2, 4, 6, 10, 0, 11, 9, 7, 5, 1, 8, 3])
    assert row.transpose(4) == new

    new = pitchtools.TwelveToneRow([3, 5, 7, 11, 1, 0, 10, 8, 6, 2, 9, 4])
    assert row.transpose(5) == new
