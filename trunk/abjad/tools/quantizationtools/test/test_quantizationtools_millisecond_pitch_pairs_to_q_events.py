from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import millisecond_pitch_pairs_to_q_events


def test_quantizationtools_millisecond_pitch_pairs_to_q_events_01( ):

   durations = [100, 200, 100, 300, 350, 400, 600]
   pitches = [0, None, None, [1, 4], None, 5, 7]
   pairs = zip(durations, pitches)

   q_events = millisecond_pitch_pairs_to_q_events(pairs)

   assert q_events == [
      QEvent(0, 100, 0), 
      QEvent(100, 300, None), 
      QEvent(400, 300, (1, 4)), 
      QEvent(700, 350, None),
      QEvent(1050, 400, 5), 
      QEvent(1450, 600, 7)]
