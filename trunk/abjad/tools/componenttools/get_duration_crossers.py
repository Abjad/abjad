from abjad.component import _Component
from abjad.rational import Rational
from abjad.tools import iterate


def get_duration_crossers(component, prolated_offset):
   r'''List all components in `component` that cross `prolated_offset`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 2/8
            e'8
            f'8
         }
      }

   Examples refer to the score above.
      
   No components cross prolated offset ``0``::
      
      abjad> componenttools.get_duration_crossers(staff, 0)
      []

   Staff, measure and leaf cross prolated offset ``1/16``::

      abjad> componenttools.get_duration_crossers(staff, Rational(1, 16))
      [Staff{2}, RigidMeasure(2/8, [c'8, d'8]), Note(c', 8)]

   Staff and measure cross prolated offset ``1/8``::

      abjad> componenttools.get_duration_crossers(staff, Rational(1, 8))
      [Staff{2}, RigidMeasure(2/8, [c'8, d'8])]

   Staff crosses prolated offset ``1/4``::

      abjad> componenttools.get_duration_crossers(staff, Rational(1, 4))
      [Staff{2}]

   No components cross prolated offset ``99``::

      abjad> componenttools.get_duration_crossers(staff, 99)
      []
   '''

   assert isinstance(component, _Component)
   assert isinstance(prolated_offset, (int, float, Rational))

   result = [ ]

   if component.duration.prolated <= prolated_offset:
      return result

   boundary_time = component.offset.prolated.start + prolated_offset

   for x in iterate.naive_forward_in(component, _Component):
      x_start = x.offset.prolated.start
      x_stop = x.offset.prolated.stop
      if x_start < boundary_time < x_stop:
         result.append(x)

   return result
