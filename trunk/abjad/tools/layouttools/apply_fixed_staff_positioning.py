from abjad.components.Measure import _Measure
from abjad.tools import componenttools
from abjad.tools.layouttools.FixedStaffPositioning import FixedStaffPositioning
from abjad.tools.layouttools.StaffAlignmentOffsets import StaffAlignmentOffsets
from abjad.tools.layouttools.StaffAlignmentDistances import StaffAlignmentDistances


def apply_fixed_staff_positioning(expr, positioning, klass = _Measure):
   r'''Apply `positioning` to `expr`.
   Music `expr` must already be marked with line breaks.

   ::

      abjad> t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> macros.diatonicize(t)
      abjad> layout.set_line_breaks_cyclically_by_line_duration_ge(t, Rational(4, 8))      
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

   ::

      abjad> systems = SystemYOffsets(40, 5)
      abjad> staves = StaffAlignmentOffsets(0, -15)
      abjad> positioning = FixedStaffPositioning(systems, staves)
      abjad> layout.apply_fixed_staff_positioning(t, positioning)
      abjad> print t.format
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

   if not isinstance(positioning, FixedStaffPositioning):
      raise TypeError

   systems_per_page = positioning.system_y_offsets.systems_per_page
   starting_system = positioning.system_y_offsets.skip_systems_on_first_page

   if positioning.staff_alignment_offsets is not None:
      try:
         alignment_values = \
            positioning.staff_alignment_offsets.alignment_offsets
      except AttributeError:
         alignment_values = \
            positioning.staff_alignment_offsets.alignment_distances
   else:
      alignment_values = [0]

   line_breaks_found = 0
   prev = None
   for cur in componenttools.iterate_components_forward_in_expr(expr, klass):
      if prev is None or prev.breaks.line:
         system_on_page = line_breaks_found + starting_system
         system_on_page %= systems_per_page
         y_offset = positioning.system_y_offsets[system_on_page]
         cur.breaks.y = y_offset
         if isinstance(positioning.staff_alignment_offsets, 
            StaffAlignmentOffsets):
            cur.breaks.alignment_offsets = alignment_values
         elif isinstance(positioning.staff_alignment_offsets, 
            StaffAlignmentDistances):
            cur.breaks.alignment_distances = alignment_values
         else:
            raise TypeError('should be alignment offsets or distances.')
         line_breaks_found += 1
         if system_on_page == 0:
            if prev is not None:
               prev.breaks.page = True
         ## TODO: Write test cases for this this branch. ##
         else:
            if prev is not None:
               prev.breaks.page = False
      prev = cur
