from abjad import *
from experimental import *


def test_Quantizer___call___01():

    ms = [1000, 500, -500, 750, 500, -250, 500]
    seq = quantizationtools.QEventSequence.from_millisecond_durations(ms)
    q = quantizationtools.Quantizer()

    result = q(seq)

    assert isinstance(result, Voice)
    assert result.prolated_duration == 1
