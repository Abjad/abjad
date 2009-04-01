from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_dominant_spanners import get_dominant_spanners
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.spanner_get_component_at_score_offset import \
   spanner_get_component_at_score_offset


def splice_after(component, new_components):
   '''Splice new_components after component.
      Return list of [component] + new_components.'''

   assert_components([component])
   assert_components(new_components)

   parent, index, stop_index = get_parent_and_indices([component])

   receipt = get_dominant_spanners([component])

   score_insert_point = component.offset.score + component.duration.prolated

   for spanner, position_index in receipt:
      insert_component = spanner_get_component_at_score_offset(
         spanner, score_insert_point)
      if insert_component is not None:
         insert_index = spanner.index(insert_component)
      else:
         insert_index = len(spanner)
      for new_component in reversed(new_components):
         spanner._insert(insert_index, new_component)
         new_component.spanners._add(spanner)

   if parent is not None:
      for new_component in reversed(new_components):
         new_component.parentage._switchParentTo(parent)
         parent._music.insert(index + 1, new_component)

   return [component] + new_components
