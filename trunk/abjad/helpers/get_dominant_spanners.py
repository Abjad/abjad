from abjad.helpers.assert_components import _assert_components
from abjad.helpers.get_attached_spanners import _get_attached_spanners
from abjad.helpers.is_dominant_spanner import _is_dominant_spanner


## TODO: Deprecate entirely in favor of get_dominant_spanners_receipt( ).
##       After deprecation, rename get_dominant_spanners_receipt( )
##       to simply _get_dominant_spanners.

def _get_dominant_spanners(components):
   '''Return list of all spanners that include all components in list.'''
   
   # check input
   _assert_components(components, contiguity = 'strict', share = 'thread')

   # get attached spanners
   attached_spanners = _get_attached_spanners(components)

   # get dominant spanners
   dominant_spanners = [
      x for x in attached_spanners if _is_dominant_spanner(x, components)]

   # return dominant spanners
   return set(dominant_spanners)
