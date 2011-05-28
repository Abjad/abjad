from abjad.components import Measure
from abjad.tools import componenttools
from abjad.tools import marktools
from abjad.tools.layouttools.FixedStaffPositioning import FixedStaffPositioning
from abjad.tools.layouttools.StaffAlignmentDistances import StaffAlignmentDistances
from abjad.tools.layouttools.StaffAlignmentOffsets import StaffAlignmentOffsets


def apply_fixed_staff_positioning(expr, positioning, klass = Measure):
   r'''Apply `positioning` to `expr`.
   Music `expr` must already be marked with line breaks.

   ::

      abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> macros.diatonicize(t)
      abjad> layout.set_line_breaks_cyclically_by_line_duration_ge(t, Fraction(4, 8))      
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

#   print ''
#   print positioning.staff_alignment_offsets.alignment_distances
#   print positioning.system_y_offsets
#   print ''

   systems_per_page = positioning.system_y_offsets.systems_per_page
   starting_system = positioning.system_y_offsets.skip_systems_on_first_page

   if positioning.staff_alignment_offsets is not None:
#      try:
#         alignment_values = positioning.staff_alignment_offsets.alignment_offsets
#      except AttributeError:
#         alignment_values = positioning.staff_alignment_offsets.alignment_distances
      alignment_values = positioning.staff_alignment_offsets.alignment_distances
   else:
      alignment_values = [0]

   line_breaks_found = 0
   prev = None
   for cur in componenttools.iterate_components_forward_in_expr(expr, klass):
      #if prev is None or prev.breaks.line:
      if prev is None or marktools.is_component_with_lilypond_command_mark_attached(prev, 'break'):
         system_on_page = line_breaks_found + starting_system
         system_on_page %= systems_per_page
         y_offset = positioning.system_y_offsets[system_on_page]
         ## TODO: update this if functionality is still desired ##
         #cur.breaks.y = y_offset
         if isinstance(positioning.staff_alignment_offsets, StaffAlignmentDistances):
            #cur.breaks.alignment_distances = alignment_values
            override_string = _make_override_string(y_offset, alignment_values)
            marktools.LilyPondCommandMark(override_string, 'before')(cur)
         else:
            raise TypeError('should be staff alignment distances.')
         line_breaks_found += 1
         if system_on_page == 0:
            if prev is not None:
               #prev.breaks.page = True
               marktools.LilyPondCommandMark('pageBreak', 'after')(prev)
         ## TODO: Write test cases for this this branch. ##
         else:
            if prev is not None:
               #prev.breaks.page = False
               marktools.LilyPondCommandMark('noPageBreak', 'after')(prev)
      prev = cur

def _make_override_string(y_offset, alignment_values):
   alignment_values = ' '.join([str(x) for x in alignment_values])
   override_string = '''overrideProperty #"Score.NonMusicalPaperColumn"
#'line-break-system-details
#'((Y-offset . %s) (alignment-distances . (%s)))''' % (
   y_offset, alignment_values)
   return override_string
