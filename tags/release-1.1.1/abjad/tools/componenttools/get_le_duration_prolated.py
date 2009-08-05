from abjad.rational import Rational
from abjad.tools import check


def get_le_duration_prolated(components, prolated_duration):
   '''Assert thread-contiguous Python list of Abjad components.
      Accumulate components from list.
      Stop when total prolated duration *just* <= 'prolated_duration'.
      Return (accumulated components, accumulated duration).'''

   check.assert_components(components, contiguity = 'thread')

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
