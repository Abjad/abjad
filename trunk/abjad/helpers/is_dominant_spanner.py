from abjad.helpers.assert_components import _assert_are_strictly_contiguous_components_in_same_thread
from abjad.spanner.spanner import Spanner


def _is_dominant_spanner(spanner, components):
   '''True when spanner 'dominates' all components in list.
      That is, True when spanner includes all components in list.'''

   ## check input
   assert isinstance(spanner, Spanner)
   _assert_are_strictly_contiguous_components_in_same_thread(components)

   if len(components) == 0:
      return False

   first = components[0]
   last = components[-1]

   return first in spanner and last in spanner 
