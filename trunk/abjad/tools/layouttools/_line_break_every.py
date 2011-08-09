from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import marktools
from abjad.tools.measuretools.Measure import Measure


def _line_break_every(expr, line_duration, klass = Measure, 
   kind = 'prolated', adjust_eol = False, add_empty_bars = False):
   '''Iterate klasses in `expr` and accumulate `kind` duration.

   Add line break after every total less than or equal to duration.

   .. versionchanged:: 1.1.1
      If `adjust_eol` is True, apply rightwards extra-offset to LilyPond
      TimeSignature and LilyPond Barline at end of line with magic Scheme.

   .. versionadded:: 1.1.2
      New `add_empty_bars` keyword.
   '''

   prev = None
   cum_duration = durtools.Duration(0)
   for cur in componenttools.iterate_components_forward_in_expr(expr, klass):
      ## compress these 4 lines to only the 4th line after duration migration
      if kind == 'seconds':
         cur_duration = cur.duration_in_seconds
      elif kind == 'prolated':
         cur_duration = cur.prolated_duration
      elif kind == 'preprolated':
         cur_duration = cur.preprolated_duration
      else:
         cur_duration = getattr(cur.duration, kind)
      candidate_duration = cum_duration + cur_duration
      if candidate_duration < line_duration:
         cum_duration += cur_duration
      elif candidate_duration == line_duration:
         marktools.LilyPondCommandMark('break', format_slot = 'closing')(cur)
         if adjust_eol:
            marktools.LilyPondCommandMark('adjustEOLTimeSignatureBarlineExtraOffset', 
               format_slot = 'closing')(cur)
         if add_empty_bars:
            if cur.bar_line.kind is None:
               cur.bar_line.kind = ''
         cum_duration = durtools.Duration(0)
      else:
         if prev is not None:
            marktools.LilyPondCommandMark('break', format_slot = 'closing')(prev)
            if adjust_eol:
               marktools.LilyPondCommandMark('adjustEOLTimeSignatureBarlineExtraOffset', 
                  format_slot = 'closing')(prev)
            if add_empty_bars:
               if cur.bar_line.kind is None:
                  cur.bar_line.kind = ''
         cum_duration = cur_duration
      prev = cur
