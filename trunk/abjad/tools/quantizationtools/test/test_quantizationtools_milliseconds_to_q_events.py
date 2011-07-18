from abjad.tools.mathtools import difference_series
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import milliseconds_to_q_events
from abjad.tools.quantizationtools._time_segments import _time_segments


def test_quantizationtools_milliseconds_to_q_events_01( ):
   '''Test basic functionality.'''

   durations = difference_series([x[0] for x in _time_segments])
   q_events = milliseconds_to_q_events(durations)

   assert all([isinstance(x, QEvent) for x in q_events])
   assert len(durations) == len(q_events)
   
   zipped = zip(durations, q_events)
   for i, pair in enumerate(zipped):
      this_duration = pair[0]
      this_q_event = pair[1]
      assert this_duration == this_q_event.duration
      if 0 < i:
         prev_duration = zipped[i - 1][0]
         prev_q_event = zipped[i - 1][1]
         assert this_q_event.offset == prev_q_event.offset + prev_q_event.duration


def test_quantizationtools_milliseconds_to_q_events_02( ):
   '''Silences are fused.'''

   durations = [100, -100, 100, -100, -100, 100]
   q_events = milliseconds_to_q_events(durations)
   assert q_events == [
      QEvent(0, 100, 0),
      QEvent(100, 100, None),
      QEvent(200, 100, 0),
      QEvent(300, 200, None),
      QEvent(500, 100, 0)]
