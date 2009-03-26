from abjad.helpers.assert_components import assert_components
from abjad.spanner.spanner import Spanner


def _is_dominant_spanner(spanner, components):
   '''True when spanner 'dominates' all components in list.
      That is, True when spanner includes all components in list.'''

   ## check input
   assert isinstance(spanner, Spanner)
   assert_components(components, contiguity = 'strict', share = 'thread')

   if len(components) == 0:
      return False

   first = components[0]
   last = components[-1]

   return first in spanner and last in spanner 
