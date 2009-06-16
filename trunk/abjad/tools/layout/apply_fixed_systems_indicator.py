from abjad.layout import FixedSystemsIndicator
from abjad.measure.measure import _Measure
from abjad.tools import iterate


def apply_fixed_systems_indicator(expr, system_indicator, klass = _Measure):
   r'''Apply *system_indicator* to *expr*.
   Music *expr* must already be marked with line breaks.

   ::

      t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
      pitchtools.diatonicize(t)
      layout.line_break_every_prolated(t, Rational(4, 8))      

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

      system_indicator = FixedSystemsIndicator((20, ), 1)
      layout.apply_fixed_systems_indicator(t, system_indicator)

      \new Staff {
                      \overrideProperty #"Score.NonMusicalPaperColumn"
                      #'line-break-system-details
                      #'((Y-offset . 20))
                      \time 2/8
                      c'8
                      d'8
                      \time 2/8
                      e'8
                      f'8
                      \break
                      \pageBreak
                      \overrideProperty #"Score.NonMusicalPaperColumn"
                      #'line-break-system-details
                      #'((Y-offset . 20))
                      \time 2/8
                      g'8
                      a'8
                      \time 2/8
                      b'8
                      c''8
                      \break
      }
   '''

   if not isinstance(system_indicator, FixedSystemsIndicator):
      raise TypeError

   y_offset_tuple = system_indicator.y_offset_tuple
   systems_per_page = len(y_offset_tuple)

   line_breaks_found = 0
   prev = None
   for cur in iterate.naive(expr, klass):
      if prev is None or prev.breaks.line:
         system_on_page = (line_breaks_found + 
            system_indicator.starting_system) % \
            systems_per_page
         y_offset = y_offset_tuple[system_on_page]
         cur.breaks.y = y_offset
         line_breaks_found += 1
         if system_on_page == 0:
            if prev is not None:
               prev.breaks.page = True
         ## TODO: Write test cases for this this branch. ##
         else:
            if prev is not None:
               prev.breaks.page = False
      prev = cur
