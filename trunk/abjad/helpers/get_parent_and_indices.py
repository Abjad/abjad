from abjad.helpers.assert_components import assert_components


def get_parent_and_indices(components):
   '''Return parent of components in list.
      Return index of first component in list in parent.
      Return inex of last component in list in parent.
      Otherwise None, None, None.'''

   assert_components(components, contiguity = 'strict', share = 'thread')

   if len(components) > 0:
      first, last = components[0], components[-1]
      parent = first.parentage.parent
      if parent is not None:
         first_index = parent.index(first)
         last_index = parent.index(last)
         return parent, first_index, last_index

   return None, None, None
