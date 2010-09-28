from abjad.components.Measure import Measure
from abjad.tools.layouttools._line_break_every import _line_break_every


def set_line_breaks_cyclically_by_line_duration_ge(expr, line_duration, klass = Measure,
   adjust_eol = False, add_empty_bars = False):
   r'''Iterate `klass` instances in `expr` and accumulate prolated duration.
   Add line break after every total less than or equal to `line_duration`.

   ::

      abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> macros.diatonicize(t)
      abjad> print t.format
      \new Staff {
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
      }

   ::

      abjad> layouttools.set_line_breaks_cyclically_by_line_duration_ge(t, Fraction(4, 8))      
      abjad> print t.format
      \new Staff {
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \break
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
                      \break
      }

   Set `adjust_eol` to ``True`` to include a magic Scheme incantation
   to move end-of-line LilyPond TimeSignature and BarLine grobs to
   the right.

   .. versionchanged:: 1.1.2
      renamed ``layout.line_break_every_prolated( )`` to
      ``layout.set_line_breaks_cyclically_by_line_duration_ge( )``.
   '''

   _line_break_every(
      expr, line_duration, klass, 'prolated', adjust_eol = adjust_eol,
      add_empty_bars = add_empty_bars)
