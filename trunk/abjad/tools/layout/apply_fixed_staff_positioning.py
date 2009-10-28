from abjad.measure.measure import _Measure
from abjad.tools import iterate
from abjad.tools.layout.FixedStaffPositioning import FixedStaffPositioning


def apply_fixed_staff_positioning(expr, positioning, klass = _Measure):
   r'''Apply `positioning` to `expr`.
   Music `expr` must already be marked with line breaks.

   ::

      abjad> t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      abjad> pitchtools.diatonicize(t)
      abjad> layout.line_break_every_prolated(t, Rational(4, 8))      
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
      alignment_offsets = \
         positioning.staff_alignment_offsets.alignment_offsets
   else:
      alignment_offsets = [0]

   line_breaks_found = 0
   prev = None
   for cur in iterate.naive_forward(expr, klass):
      if prev is None or prev.breaks.line:
         system_on_page = line_breaks_found + starting_system
         system_on_page %= systems_per_page
         y_offset = positioning.system_y_offsets[system_on_page]
         cur.breaks.y = y_offset
         cur.breaks.alignment_offsets = alignment_offsets
         line_breaks_found += 1
         if system_on_page == 0:
            if prev is not None:
               prev.breaks.page = True
         ## TODO: Write test cases for this this branch. ##
         else:
            if prev is not None:
               prev.breaks.page = False
      prev = cur
