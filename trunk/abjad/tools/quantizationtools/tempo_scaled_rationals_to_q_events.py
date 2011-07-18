from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import Duration
from abjad.tools.durtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.seqtools import sum_consecutive_sequence_elements_by_sign


def tempo_scaled_rationals_to_q_events(durations, tempo):

   assert all([isinstance(x, (int, Fraction)) for x in durations])
   assert isinstance(tempo, TempoMark)

   durations = filter(None, sum_consecutive_sequence_elements_by_sign(durations, sign = [-1]))
   durations = [tempo_scaled_rational_to_milliseconds(x, tempo) for x in durations]

   offsets = cumulative_sums_zero([abs(x) for x in durations])

   q_events = [ ]
   for pair in zip(offsets, durations):
      if pair[1] < 0: # negative duration indicates silence
         q_event = QEvent(Offset(pair[0]), Duration(abs(pair[1])), None)
      else:
         q_event = QEvent(Offset(pair[0]), Duration(pair[1]), 0)
      q_events.append(q_event)

   return q_events
