from abjad.helpers.assert_components import assert_components
from abjad.rational.rational import Rational


def get_components_le_prolated_duration(components, prolated_duration):
   '''Assert thread-contiguous Python list of Abjad components.
      Accumulate components from list.
      Stop when total prolated duration *just* <= 'prolated_duration'.
      Return (accumulated components, accumulated duration).'''

   assert_components(components, contiguity = 'thread')

   total_duration = Rational(0)
   result = [ ]
   for component in components:
      cur_duration = component.duration.prolated
      if total_duration + cur_duration <= prolated_duration:
         result.append(component)
         total_duration += cur_duration
      else:
         break

   return result, total_duration
