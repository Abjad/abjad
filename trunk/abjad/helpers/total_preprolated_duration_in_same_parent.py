from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_strictly_contiguous_components_in_same_parent import _are_strictly_contiguous_components_in_same_parent


def _total_preprolated_duration_in_same_parent(components):
   '''Components must be strictly contiguous and in same parent.

      Return sum of preprolated duration of all components in list.'''

   ## check input
   if not _are_strictly_contiguous_components_in_same_parent(components):
      raise ContiguityError(
         'Input must be strictly contiguous components in same parent.')

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
