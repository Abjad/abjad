from abjad.helpers.are_successive_components import _are_successive_components
from abjad.spanner.spanner import Spanner


def _is_dominant_spanner(spanner, component_list):
   '''True when spanner 'dominates' all components in list;
      that is, True when spanner includes all components in list.'''

   assert isinstance(spanner, Spanner)
   if not _are_successive_components(component_list):
      raise ContiguityError('components must be successive.')

   if len(component_list) == 0:
      return False

   first = component_list[0]
   last = component_list[-1]

   return first in spanner and last in spanner 
