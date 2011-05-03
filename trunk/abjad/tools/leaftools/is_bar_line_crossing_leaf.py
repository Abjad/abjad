from fractions import Fraction
from abjad.tools import contexttools


def is_bar_line_crossing_leaf(leaf):
   r'''.. versionadded:: 1.1.2

   True when `leaf` crosses bar line::

      abjad> t = Staff(macros.scale(4))
      abjad> t[2].duration.written *= 2
      abjad> contexttools.TimeSignatureMark(2, 8, partial = Fraction(1, 8))(t[2])
      abjad> f(t)
      \new Staff {
              \time 2/8
              \partial 8
              c'8
              d'8
              e'4
              f'8
      }
      abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[2])
      True

   Otherwise false::

      abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[3])
      False

   Return boolean.
   '''

   meter = contexttools.get_effective_time_signature(leaf)
   partial = meter.partial
   if meter.partial is None:
      partial = Fraction(0)

   shifted_start = (leaf._offset.start - partial) % meter.duration
   shifted_stop = (leaf._offset.stop - partial) % meter.duration

   if meter.duration < shifted_start + leaf.duration.prolated:
      return True

   return False
