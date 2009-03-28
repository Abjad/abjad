from abjad.component.component import _Component
from abjad.exceptions.exceptions import NegativeDurationError
from abjad.helpers.get_components_le_prolated_duration import \
   get_components_le_prolated_duration
from abjad.helpers.leaf_duration_change import leaf_duration_change
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


## TODO: Generalize to trim on either left or right edge. ##
## TODO: Generalize to trim in the middle. ##

def component_trim_by_duration(component, duration):
   '''Trim the first 'duration' of time from 'component'.
      When 'component' is a leaf, shorten duration of leaf.
      When 'component' is a container, remove contents from container.
      Add ties or duration-modification tuplets as necessary.
      Return value to be determined.
      Maybe return ejected components.'''

   assert isinstance(component, _Component)
   assert isinstance(duration, Rational)

   if component.duration.prolated <= duration:
      raise NegativeDurationError('component durations must be positive.')

   ## TODO: Allow big trimming value to empty containers. ##

   if isinstance(component, _Leaf):
      new_prolated_duration = component.duration.prolated - duration
      prolation = component.duration.prolation
      new_written_duration = new_prolated_duration / prolation
      result = leaf_duration_change(component, new_written_duration)
   else:
      container = component
      components, accumulated_duration = get_components_le_prolated_duration(
         container[:], duration)
      del(container[:len(components)])
      remaining_subtrahend_duration = duration - accumulated_duration
      component_trim_by_duration(container[0], remaining_subtrahend_duration)
