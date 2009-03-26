from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_dominant_spanners import get_dominant_spanners
from abjad.helpers.get_parent_and_index import get_parent_and_index


def splice_after(component, new_components):
   '''Splice new_components after component.
      Return list of [component] + new_components.'''

   assert_components([component])
   assert_components(new_components)

   parent, index = get_parent_and_index([component])

   if parent is not None:
      for new_component in reversed(new_components):
         new_component.parentage._switchParentTo(parent)
         parent._music.insert(index + 1, new_component)

   receipt = get_dominant_spanners([component])

   for spanner, index in receipt:
      for new_component in reversed(new_components):
         spanner._insert(index + 1, new_component)
         new_component.spanners._add(spanner)

   return [component] + new_components
