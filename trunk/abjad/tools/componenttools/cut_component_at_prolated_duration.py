from abjad.components._Component import _Component
from abjad.components._Leaf import _Leaf
from abjad.exceptions import NegativeDurationError
from abjad.tools.componenttools.list_leftmost_components_with_prolated_duration_at_most import list_leftmost_components_with_prolated_duration_at_most
from fractions import Fraction


## TODO: implement related function to cut from right edge.
## TODO: implement related function to cut in middle.
## TODO: allow large values of `prolated_duration` to empty container contents.
def cut_component_at_prolated_duration(component, prolated_duration):
   r'''.. versionadded:: 1.1.2

   Cut `component` at dotted `prolated_duration`::

      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> componenttools.cut_component_at_prolated_duration(staff, Fraction(1, 32))
      abjad> f(staff)
      \new Staff {
         c'16. [
         d'8
         e'8
         f'8 ]
      }
      
   Cut `component` at tied `prolated_duration`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> componenttools.cut_component_at_prolated_duration(staff, Fraction(3, 64))
      abjad> f(staff)
      \new Staff {
         c'16 [ ~
         c'64
         d'8
         e'8
         f'8 ]
      }
      
   Cut `component` at nonbinary `prolated_duration`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> componenttools.cut_component_at_prolated_duration(staff, Fraction(1, 24))
      abjad> f(staff)
      \new Staff {
         \times 2/3 {
            c'8 [
         }
         d'8
         e'8
         f'8 ]
      }

   Return none.
   '''
   from abjad.tools import leaftools

   assert isinstance(component, _Component)
   assert isinstance(prolated_duration, Fraction)

   if component.duration.prolated <= prolated_duration:
      raise NegativeDurationError('component durations must be positive.')

   if isinstance(component, _Leaf):
      new_prolated_duration = component.duration.prolated - prolated_duration
      prolation = component.duration.prolation
      new_written_duration = new_prolated_duration / prolation
      result = leaftools.set_preprolated_leaf_duration(
         component, new_written_duration)
   else:
      container = component
      components, accumulated_duration = \
         list_leftmost_components_with_prolated_duration_at_most(
         container[:], prolated_duration)
      del(container[:len(components)])
      remaining_subtrahend_duration = prolated_duration - accumulated_duration
      cut_component_at_prolated_duration(container[0], remaining_subtrahend_duration)
