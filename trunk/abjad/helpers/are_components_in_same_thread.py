from abjad.component.component import _Component


def _are_components_in_same_thread(component_list):
   if isinstance(component_list, list):
      if len(component_list) == 0:
         return True
      first = component_list[0]
      if isinstance(first, _Component):
         signature = first.parentage._threadSignature
         for component in component_list[1:]:
            if component.parentage._threadSignature != signature:
               return False
         return True
   return False
