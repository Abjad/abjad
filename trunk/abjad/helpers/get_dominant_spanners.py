from abjad.helpers.are_successive_components import _are_successive_components
from abjad.helpers.get_attached_spanners import _get_attached_spanners
from abjad.helpers.is_dominant_spanner import _is_dominant_spanner


def _get_dominant_spanners(component_list):
   '''Return list of all spanners that include all components in list.'''
   
   # check input
   if not _are_successive_components(component_list):
      raise ContiguityError('components must be successive.')

   # get attached spanners
   attached_spanners = _get_attached_spanners(component_list)

   # get dominant spanners
   dominant_spanners = [
      x for x in attached_spanners if _is_dominant_spanner(x, component_list)]

   # return dominant spanners
   return set(dominant_spanners)
