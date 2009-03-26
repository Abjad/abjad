from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.assert_components import assert_components


def _total_preprolated_duration_in_same_parent(components):
   '''Components must be strictly contiguous and in same parent.

      Return sum of preprolated duration of all components in list.'''

   ## check input
   assert_components(components, contiguity = 'strict', share = 'parent')

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
