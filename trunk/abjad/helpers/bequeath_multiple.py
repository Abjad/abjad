from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.assert_components import assert_components
from abjad.helpers.components_detach_spanners_shallow import \
   _components_detach_spanners_shallow
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to
from abjad.helpers.get_dominant_spanners import get_dominant_spanners
from abjad.helpers.get_parent_and_index import get_parent_and_index


#def bequeath_multiple(old_components, new_components):
#   '''Bequeath position-in-spanners and position-in-parent of
#      old_components to new_components.
#
#      Prior to bequeathal both
#
#         * old components must be strictly contiguous and in same parent,
#         * new components must be either orphan or strictly contiguous
#           and in same parent.
#
#      After bequeathal
#
#         * old components are unspanned orphans, and
#         * new components are (possibly) spanned and parented.
#
#      Return orphan, unspanned old components.
#
#      Intended to let you swap an arbitrary list of successive
#      components with some other arbitrary list of orphan components.
#      For example, swap out three successive leaves with a tuplet.'''
#
#   ## check input
#   assert_components(old_components, contiguity = 'strict', share = 'parent')
#   assert_components(new_components, contiguity = 'strict', share = 'parent')
#
#   ## handle empty input
#   if len(old_components) == 0:
#      return old_components
#
#   ## detach new components from parentage
#   _components_switch_parent_to(new_components, None)
#
#   ## get dominant spanners
#   dominant_spanners = get_dominant_spanners(old_components)
#   print dominant_spanners
#   
#   ## insert new components in dominant spanners
#   for dominant_spanner, index in dominant_spanners:
#      print dominant_spanner, index
#      dominant_spanner._components[index:index] = new_components
#   for component in new_components:
#      component.spanners._update([x[0] for x in dominant_spanners])
#
#   ## unspan old components
#   _components_detach_spanners_shallow(old_components)
#
#   ## remember parent and index
#   parent, index = get_parent_and_index(old_components)
#
#   ## orphan old components
#   _components_switch_parent_to(old_components, None)
#
#   ## if parent
#   if parent is not None:
#
#      ## insert new components in parent of old components
#      for new_component in reversed(new_components):
#         new_component.parentage.parent = parent
#         parent._music.insert(index, new_component)
#
#   ## return old components
#   return old_components
