from abjad.measure import _Measure
from abjad.rational import Rational
from abjad.tools import iterate


def _line_break_every(expr, line_duration, klass = _Measure, 
   kind = 'prolated', adjust_eol = False):
   '''Iterate klasses in `expr` and accumulate `kind` duration.

   Add line break after every total less than or equal to duration.

   .. versionchanged:: 1.1.1
      If `adjust_eol` is True, apply rightwards extra-offset to LilyPond
      TimeSignature and LilyPond Barline at end of line with magic Scheme.
   '''

   prev = None
   cum_duration = Rational(0)
   for cur in iterate.naive_forward(expr, klass):
      cur_duration = getattr(cur.duration, kind)
      candidate_duration = cum_duration + cur_duration
      if candidate_duration < line_duration:
         cum_duration += cur_duration
      elif candidate_duration == line_duration:
         cur.breaks.line = True
         if adjust_eol:
            cur.breaks.eol_adjustment = True
         cum_duration = Rational(0)
      else:
         if prev is not None:
            prev.breaks.line = True
            if adjust_eol:
               prev.breaks.eol_adjustment = True
         cum_duration = cur_duration
      prev = cur
