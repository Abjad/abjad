from abjad.helpers.assert_components import _assert_are_strictly_contiguous_components_in_same_thread


def _get_parent_and_index(components):
   '''Return parent and index of first component in list.
      Otherwise return None, None.'''

   ## check input
   _assert_are_strictly_contiguous_components_in_same_thread(components)

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
