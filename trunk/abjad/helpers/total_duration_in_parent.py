from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.contiguity import _are_contiguous_music_elements


def _total_duration_in_parent(ll, parent):
   '''Return sum of preprolated duration of each element in ll
      multiplied by any multiplier of parent of ll.'''

   if not _are_contiguous_music_elements(ll):
      raise ContiguityError('Input must be contiguous music elements.')

   result = 0
   for element in ll:
      result += element.duration.preprolated
   result *= getattr(parent.duration, 'multiplier', 1)

   return result
