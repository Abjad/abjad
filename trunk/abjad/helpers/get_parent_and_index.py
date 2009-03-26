from abjad.helpers.assert_components import assert_components


def _get_parent_and_index(components):
   '''Return parent and index of first component in list.
      Otherwise return None, None.'''

   ## check input
   assert_components(components, contiguity = 'strict', share = 'thread')

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
