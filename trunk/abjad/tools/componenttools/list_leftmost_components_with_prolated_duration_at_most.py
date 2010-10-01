from fractions import Fraction


def list_leftmost_components_with_prolated_duration_at_most(components, prolated_duration):
   '''Return tuple of ``components[:i]`` together with 
   the prolated duration of ``components[:i]``. ::

      abjad> voice = Voice(macros.scale(4))
      abjad> componenttools.list_leftmost_components_with_prolated_duration_at_most(voice[:], Fraction(1, 4))
      ([Note(c', 8), Note(d', 8)], Fraction(1, 4))

   Maximize ``i`` such that the prolated duration of 
   ``components[:i]`` is no greater than `prolated_duration`.

   Input `components` must be thread-contiguous.

   .. todo:: implement
      ``componenttools.list_leftmost_components_with_prolated_duration_at_least( )``.

   .. todo:: implement
      ``componenttools.list_rightmost_components_with_prolated_duration_at_most( )``.

   .. todo:: implement
      ``componenttools.list_rightmost_components_with_prolated_duration_at_least( )``.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_le_duration_prolated( )`` to
      ``componenttools.list_leftmost_components_with_prolated_duration_at_most( )``.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_thread_contiguous_components(components)

   total_duration = Fraction(0)
   result = [ ]
   for component in components:
      cur_duration = component.duration.prolated
      if total_duration + cur_duration <= prolated_duration:
         result.append(component)
         total_duration += cur_duration
      else:
         break

   return result, total_duration
