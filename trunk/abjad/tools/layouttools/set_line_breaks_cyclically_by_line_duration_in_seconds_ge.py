from abjad.components.Measure import Measure
from abjad.tools.layouttools._line_break_every import _line_break_every


def set_line_breaks_cyclically_by_line_duration_in_seconds_ge(expr, line_duration, klass = Measure,
   adjust_eol = False, add_empty_bars = False):
   r'''Iterate `klass` instances in `expr` and accumulate duration in seconds.
   Add line break after every total less than or equal to `line_duration`.

   ::

      abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> macros.diatonicize(t)
      abjad> tempo_mark = contexttools.TempoMark(Fraction(1, 8), 44, target_context = Staff)(t)
      abjad> print t.format
      \new Staff {
                      \time 2/8
                      \tempo 8=44
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

      abjad> layouttools.set_line_breaks_cyclically_by_line_duration_in_seconds_ge(t, Fraction(6))
      abjad> print t.format
      \new Staff {
                      \time 2/8
                      \tempo 8=44
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
      }

   Set ``adjust_eol = True`` to include a magic Scheme incantation
   to move end-of-line LilyPond TimeSignature and BarLine grobs to
   the right.

   .. versionchanged:: 1.1.2
      renamed ``layout.line_break_every_seconds( )`` to
      ``layout.set_line_breaks_cyclically_by_line_duration_in_seconds_ge( )``.
   '''

   _line_break_every(
      expr, line_duration, klass, 'seconds', adjust_eol = adjust_eol,
      add_empty_bars = add_empty_bars)
