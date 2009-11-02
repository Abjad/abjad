from abjad.tools.layout.LayoutSchema import LayoutSchema
from abjad.tools.layout.apply_fixed_staff_positioning import \
   apply_fixed_staff_positioning
from abjad.tools.layout.line_break_every_prolated import \
   line_break_every_prolated


def apply_layout_schema(expr, layout_schema, adjust_eol = False):
   r'''.. versionadded:: 1.1.2

   Apply `layout_schema` to `expr`.

   The following example line breaks every 4 eighth notes,
   layos out 5 systems per page, spaces systems 40 vertical spaces
   apart, leaves empty vertical space equivalent to a single system
   at the top of the first page, and sets the two staves in each system
   at offsets 0 and -15. ::

      abjad> t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      abjad> pitchtools.diatonicize(t)
      abjad> schema = Layout(Rational(4, 8), (40, 5, 1), (0, -15))
      abjad> layout.apply_layout_schema(t, schema)
      abjad> f(t)
      \new Staff {
              {
                      \overrideProperty #"Score.NonMusicalPaperColumn"
                      #'line-break-system-details
                      #'((Y-offset . 40) (alignment-offsets . (0 -15)))
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
                      #'((Y-offset . 80) (alignment-offsets . (0 -15)))
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
   '''
   
   if not isinstance(layout_schema, LayoutSchema):
      raise TypeError('must be layout schema.')

   line_break_every_prolated(
      expr, layout_schema.line_break_duration, adjust_eol = adjust_eol)
   apply_fixed_staff_positioning(expr, layout_schema.fixed_staff_positioning)
