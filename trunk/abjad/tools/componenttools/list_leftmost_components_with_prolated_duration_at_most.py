from abjad.rational import Rational
from abjad.tools import check


def list_leftmost_components_with_prolated_duration_at_most(components, prolated_duration):
   '''Return tuple of ``components[:i]`` together with 
   the prolated duration of ``components[:i]``. ::

      abjad> voice = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> componenttools.list_leftmost_components_with_prolated_duration_at_most(voice[:], Rational(1, 4))
      ([Note(c', 8), Note(d', 8)], Rational(1, 4))

   Maximize ``i`` such that the prolated duration of 
   ``components[:i]`` is no greater than `prolated_duration`.

   Input `components` must be thread-contiguous.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_le_duration_prolated( )`` to
      ``componenttools.list_leftmost_components_with_prolated_duration_at_most( )``.
   '''

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
