from abjad.tools.contexttools import TempoMark
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import difference_series
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds
from abjad.tools.quantizationtools import tempo_scaled_rationals_to_q_events


def test_quantizationtools_tempo_scaled_rationals_to_q_events_01():
    '''Test basic functionality.'''

    durations = [Duration(x) for x in [(1, 4), (1, 3), (1, 7), (2, 5), (3, 4)]]
    tempo = TempoMark((1, 4), 55)
    q_events = tempo_scaled_rationals_to_q_events(durations, tempo)

    assert q_events == [
        QEvent(Offset(0, 1), 0),
        QEvent(Offset(12000, 11), 0),
        QEvent(Offset(28000, 11), 0),
        QEvent(Offset(244000, 77), 0),
        QEvent(Offset(34400, 7), 0),
        QEvent(Duration(630400, 77), None)]


def test_quantizationtools_tempo_scaled_rationals_to_q_events_02():
    '''Silences are fused.'''

    durations = [Duration(x) for x in [(1, 4), (-1, 4), (1, 4), (1, 4), (-1, 4), (-1, 4), (1, 4)]]
    tempo = TempoMark((1, 4), 77)
    q_events = tempo_scaled_rationals_to_q_events(durations, tempo)
    assert q_events == [
        QEvent(Offset(0, 1), 0),
        QEvent(Offset(60000, 77), None),
        QEvent(Offset(120000, 77), 0),
        QEvent(Offset(180000, 77), 0),
        QEvent(Offset(240000, 77), None),
        QEvent(Offset(360000, 77), 0),
        QEvent(Duration(60000, 11), None)]
