from abjad.tools.durtools import Offset
from abjad.tools.mathtools import cumulative_sums_zero
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.seqtools import sum_consecutive_sequence_elements_by_sign


def milliseconds_to_q_events(milliseconds):

   durations = filter(None, sum_consecutive_sequence_elements_by_sign(milliseconds, sign = [-1]))
   offsets = cumulative_sums_zero([abs(x) for x in durations])

   q_events = [ ]
   for pair in zip(offsets, durations):
      offset = Offset(pair[0])
      duration = pair[1]
      if duration < 0: # negative duration indicates silence
         q_event = QEvent(offset, None)
      else:
         q_event = QEvent(offset, 0)
      q_events.append(q_event)

   # insert terminating silence
   q_events.append(QEvent(Offset(offsets[-1]), None))

   return q_events
