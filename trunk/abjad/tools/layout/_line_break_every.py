from abjad.measure.measure import _Measure
from abjad.rational import Rational
from abjad.tools import iterate


def _line_break_every(expr, line_duration, klass = _Measure, kind = 'prolated'):
   '''Iterate klasses in expr and accumulate 'kind' duration.
      Add line break after every total less than or equal to duration.'''

   prev = None
   cum_duration = Rational(0)
   for cur in iterate.naive(expr, klass):
      cur_duration = getattr(cur.duration, kind)
      candidate_duration = cum_duration + cur_duration
      if candidate_duration < line_duration:
         cum_duration += cur_duration
      elif candidate_duration == line_duration:
         cur.breaks.line = True
         cum_duration = Rational(0)
      else:
         if prev is not None:
            prev.breaks.line = True
         cum_duration = cur_duration
      prev = cur
