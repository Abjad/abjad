from abjad.helpers.is_assignable import _is_assignable
from abjad.leaf.leaf import _Leaf


def _are_scalable_components(component_list, multiplier):
   '''True when all components in component_list can 
      rewrite according to multiplier with no ad hoc tuplets.'''

   for component in component_list:
      if isinstance(component, _Leaf):
         candidate_duration = multiplier * component.duration.written 
         if not _is_assignable(candidate_duration):
            return False         

   return True
