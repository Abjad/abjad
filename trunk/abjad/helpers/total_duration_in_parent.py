from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_contiguous_components import _are_contiguous_components


def _total_duration_in_parent(ll, parent):
   '''Return sum of preprolated duration of each element in ll
      multiplied by any multiplier of parent of ll.'''

   if not _are_contiguous_components(ll):
      raise ContiguityError('Input must be contiguous components.')

   result = 0
   for element in ll:
      result += element.duration.preprolated
   result *= getattr(parent.duration, 'multiplier', 1)

   return result
