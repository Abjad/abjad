from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import Duration
from abjad.tools.durtools import Offset
from abjad.tools.mathtools import difference_series
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds
from abjad.tools.quantizationtools import tempo_scaled_rationals_to_q_events


def test_quantizationtools_tempo_scaled_rationals_to_q_events_01( ):
   '''Test basic functionality.'''

   durations = [Duration(x) for x in [(1, 4), (1, 3), (1, 7), (2, 5), (3, 4)]]
   tempo = TempoMark((1, 4), 55)
   q_events = tempo_scaled_rationals_to_q_events(durations, tempo)

   assert all([isinstance(x, QEvent) for x in q_events])
   assert len(durations) == len(q_events)
   
   zipped = zip(durations, q_events)
   for i, pair in enumerate(zipped):
      this_duration = pair[0]
      this_q_event = pair[1]
      assert tempo_scaled_rational_to_milliseconds(this_duration, tempo) == this_q_event.duration
      if 0 < i:
         prev_duration = zipped[i - 1][0]
         prev_q_event = zipped[i - 1][1]
         assert this_q_event.offset == prev_q_event.offset + prev_q_event.duration


def test_quantizationtools_tempo_scaled_rationals_to_q_events_02( ):
   '''Silences are fused.'''

   durations = [Duration(x) for x in [(1, 4), (-1, 4), (1, 4), (1, 4), (-1, 4), (-1, 4), (1, 4)]]
   tempo = TempoMark((1, 4), 77)
   q_events = tempo_scaled_rationals_to_q_events(durations, tempo)
   assert q_events == [
      QEvent(Offset(0, 1), Duration(60000, 77), 0),
      QEvent(Offset(60000, 77), Duration(60000, 77), None),
      QEvent(Offset(120000, 77), Duration(60000, 77), 0),
      QEvent(Offset(180000, 77), Duration(60000, 77), 0),
      QEvent(Offset(240000, 77), Duration(120000, 77), None),
      QEvent(Offset(360000, 77), Duration(60000, 77), 0)]
