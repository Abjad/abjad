from abjad.measure.measure import _Measure
from abjad.tools.layout._line_break_every import _line_break_every


def line_break_every_seconds(expr, line_duration, klass = _Measure):
   '''Iterate klasses in expr and accumulate prolated duration.
      Add line break after every total less than or equal to line_duration.'''

   _line_break_every(expr, line_duration, klass, 'seconds')
