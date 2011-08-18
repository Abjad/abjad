from abjad import *
from abjad.tools import layouttools


def test_SpacingIndication___eq___01():
    '''Spacing indications compare equal when
        normalized spacing durations compare equal.'''

    tempo_indication = contexttools.TempoMark(Duration(1, 8), 38)
    p = layouttools.SpacingIndication(tempo_indication, Duration(1, 68))

    tempo_indication = contexttools.TempoMark(Duration(1, 4), 76)
    q = layouttools.SpacingIndication(tempo_indication, Duration(1, 68))

    assert p == q


def test_SpacingIndication___eq___02():
    '''Spacing indications compare not equal when
        normalized spacing durations compare not equal.'''

    tempo_indication = contexttools.TempoMark(Duration(1, 8), 38)
    p = layouttools.SpacingIndication(tempo_indication, Duration(1, 68))

    tempo_indication = contexttools.TempoMark(Duration(1, 8), 38)
    q = layouttools.SpacingIndication(tempo_indication, Duration(1, 78))

    assert p != q
