from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread
from abjad.helpers.get_attached_spanners import _get_attached_spanners
from abjad.helpers.is_dominant_spanner import _is_dominant_spanner


def _get_dominant_spanners(components):
   '''Return list of all spanners that include all components in list.'''
   
   # check input
   if not _are_orphan_components(components) and \
      not _are_strictly_contiguous_components_in_same_thread(components):
      raise ContiguityError(
         'Input must either be orphan components '
         'or else be strictly contiguous components in same thread.')

   # get attached spanners
   attached_spanners = _get_attached_spanners(components)

   # get dominant spanners
   dominant_spanners = [
      x for x in attached_spanners if _is_dominant_spanner(x, components)]

   # return dominant spanners
   return set(dominant_spanners)
