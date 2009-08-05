from abjad.component.component import _Component
from abjad.rational import Rational
from abjad.tools import iterate


def get_duration_crossers(component, duration):


   assert isinstance(component, _Component)
   assert isinstance(duration, (int, float, Rational))

   result = [ ]

   if component.duration.prolated <= duration:
      return result

   boundary_time = component.offset.prolated.start + duration

   for x in iterate.naive(component, _Component):
      x_start = x.offset.prolated.start
      x_stop = x.offset.prolated.stop
      if x_start < boundary_time < x_stop:
         result.append(x)

   return result
