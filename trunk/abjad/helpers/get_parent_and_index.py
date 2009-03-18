from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread


def _get_parent_and_index(components):
   '''Return parent and index of first component in list.
      Otherwise return None, None.'''

   ## check input
   if not _are_orphan_components(components) and \
      not _are_strictly_contiguous_components_in_same_thread(components):
      raise ContiguityError(
         'Input must either be orphan components or else '
         'be strictly contiguous components in same thread.')

   if len(components) > 0:
      first = components[0]
      first_parent = first.parentage.parent
      if first_parent is not None:
         index = first_parent.index(first)
      else:
         index = None
      return first_parent, index
   else:
      return None, None
