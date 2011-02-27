from abjad.components import Measure
from abjad.tools.layouttools.LayoutSchema import LayoutSchema
from abjad.tools.layouttools.apply_fixed_staff_positioning import apply_fixed_staff_positioning
from abjad.tools.layouttools.set_line_breaks_cyclically_by_line_duration_ge import \
   set_line_breaks_cyclically_by_line_duration_ge
from abjad.tools.layouttools.set_line_breaks_cyclically_by_line_duration_in_seconds_ge import \
   set_line_breaks_cyclically_by_line_duration_in_seconds_ge


def apply_layout_schema(expr, layout_schema, 
   klass = Measure, adjust_eol = False, add_empty_bars = False):
   r""".. versionadded:: 1.1.2

   Apply `layout_schema` to `expr`.

   The following example line breaks every 4 eighth notes,
   lays out 5 systems per page, spaces systems 40 vertical spaces
   apart, leaves empty vertical space equivalent to a single system
   at the top of the first page, sets the first staff in each system
   to alignment distance 0 and sets the second staff in each
   system to alignment distance 15. ::

      abjad> score = Score(2 * Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4))
      abjad> macros.diatonicize(score)
      abjad> schema = layouttools.LayoutSchema(Fraction(4, 8), (40, 5, 1), (15, ))
      abjad> layouttools.apply_layout_schema(score[0], schema)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      {
                              \overrideProperty #"Score.NonMusicalPaperColumn"
                              #'line-break-system-details
                              #'((Y-offset . 40) (alignment-distances . (15)))
                              \time 2/8
                              c'8
                              d'8
                      }
                      {
                              \time 2/8
                              e'8
                              f'8
                              \break
                              \noPageBreak
                      }
                      {
                              \overrideProperty #"Score.NonMusicalPaperColumn"
                              #'line-break-system-details
                              #'((Y-offset . 80) (alignment-distances . (15)))
                              \time 2/8
                              g'8
                              a'8
                      }
                      {
                              \time 2/8
                              b'8
                              c''8
                              \break
                      }
              }
              \new Staff {
                      {
                              \time 2/8
                              d''8
                              e''8
                      }
                      {
                              \time 2/8
                              f''8
                              g''8
                      }
                      {
                              \time 2/8
                              a''8
                              b''8
                      }
                      {
                              \time 2/8
                              c'''8
                              d'''8
                      }
              }
      >>

   .. todo:: document LayoutSchema.in_seconds.
   """
   
   if not isinstance(layout_schema, LayoutSchema):
      raise TypeError('must be layout schema.')

   if layout_schema.in_seconds:
      set_line_breaks_cyclically_by_line_duration_in_seconds_ge(expr, layout_schema.line_break_duration, 
         klass = klass, adjust_eol = adjust_eol, 
         add_empty_bars = add_empty_bars)
   else:
      set_line_breaks_cyclically_by_line_duration_ge(expr, layout_schema.line_break_duration, 
         klass = klass, adjust_eol = adjust_eol,
         add_empty_bars = add_empty_bars)

   apply_fixed_staff_positioning(expr, layout_schema.fixed_staff_positioning,
      klass = klass)
