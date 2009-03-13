from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.are_successive_components import _are_successive_components
from abjad.helpers.components_parentage_detach import components_parentage_detach
from abjad.helpers.components_unspan_shallow import components_unspan_shallow
from abjad.helpers.get_dominant_spanners import _get_dominant_spanners
from abjad.helpers.get_parent_and_index import _get_parent_and_index
from abjad.helpers.make_orphan_components import _make_orphan_components


def bequeath_multiple(old_components, new_components):
   '''Bequeath position-in-spanners and position-in-parent of
      old_components to new_components.

      Prior to bequeathal both

         * old components must be successive, and
         * new components must be successive.

      After bequeathal

         * old components are unspanned orphans, and
         * new components are (possibly) spanned and parented.

      Return orphan, unspanned old components.

      Intended to let you swap an arbitrary list of successive
      components with some other arbitrary list of orphan components.
      For example, swap out three successive leaves with a tuplet.'''

   # check input
   if not _are_successive_components(old_components):
      raise ContiguityError('old_components must be successive.')
   if not _are_successive_components(new_components):
      raise ContiguityError('new_components must be successive.')

   # handle empty input
   if len(old_components) == 0:
      return old_components

   # detach new components from parentage
   components_parentage_detach(new_components, level = 'top')

   # get dominant spanners
   dominant_spanners = _get_dominant_spanners(old_components)
   
   # insert new components in dominant spanners
   for dominant_spanner in dominant_spanners:
      index = dominant_spanner.index(old_components[0])
      dominant_spanner[index:index] = new_components

   # unspan old components
   components_unspan_shallow(old_components)

   # remember parent and index
   parent, index = _get_parent_and_index(old_components)

   # orphan old components
   _make_orphan_components(old_components)

   # if parent
   if parent is not None:

      # insert new components in parent of old components
      for new_component in reversed(new_components):
         new_component.parentage.parent = parent
         parent._music.insert(index, new_component)

   # return old components
   return old_components
