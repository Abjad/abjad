from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_NonreducedFraction___add___01():

    result = NonreducedFraction(1, 4) + NonreducedFraction(2, 8)
    assert result.pair == (4, 8)

    result = NonreducedFraction(2, 8) + NonreducedFraction(1, 4)
    assert result.pair == (4, 8)


def test_NonreducedFraction___add___02():

    result = NonreducedFraction(3, 3) + 1
    assert result.pair == (6, 3)

    result = 1 + NonreducedFraction(3, 3)
    assert result.pair == (6, 3)
