from abjad.helpers.are_successive_components import _are_successive_components


def _get_parent_and_index(component_list):
   '''Return parent and index of first component in list;
      otherwise return None, None.'''

   if not _are_successive_components(component_list):
      raise ContiguityError('components must be successive.')

   if len(component_list) > 0:
      first = component_list[0]
      parent = first.parentage.parent
      if parent is not None:
         index = parent.index(first)
      else:
         index = None
      return parent, index
   else:
      return None, None
