from abjad.component import _Component
from abjad.exceptions import NegativeDurationError
from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.tools import componenttools
from abjad.tools import leaftools


def by_prolated_duration(component, prolated_duration):
   r'''Cut `component` by dotted `prolated_duration`::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> cut.by_prolated_duration(staff, Rational(1, 32))
      abjad> f(staff)
      \new Staff {
         c'16. [
         d'8
         e'8
         f'8 ]
      }
      
   Cut `component` by tied `prolated_duration`::
      
      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> cut.by_prolated_duration(staff, Rational(3, 64))
      abjad> f(staff)
      \new Staff {
         c'16 [ ~
         c'64
         d'8
         e'8
         f'8 ]
      }
      
   Cut `component` by nonbinary `prolated_duration`::
      
      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> cut.by_prolated_duration(staff, Rational(1, 24))
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

   .. todo:: implement related function to cut from right edge.

   .. todo:: implement related function to cut in middle.

   .. todo:: allow large values of `prolated_duration` to empty
      container contents.
   '''

   assert isinstance(component, _Component)
   assert isinstance(prolated_duration, Rational)

   if component.duration.prolated <= prolated_duration:
      raise NegativeDurationError('component durations must be positive.')

   if isinstance(component, _Leaf):
      new_prolated_duration = component.duration.prolated - prolated_duration
      prolation = component.duration.prolation
      new_written_duration = new_prolated_duration / prolation
      result = leaftools.change_leaf_preprolated_duration(
         component, new_written_duration)
   else:
      container = component
      components, accumulated_duration = \
         componenttools.get_le_duration_prolated(
         container[:], prolated_duration)
      del(container[:len(components)])
      remaining_subtrahend_duration = prolated_duration - accumulated_duration
      by_prolated_duration(container[0], remaining_subtrahend_duration)
