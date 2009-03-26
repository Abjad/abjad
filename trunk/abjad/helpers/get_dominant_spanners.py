from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_attached_spanners import get_attached_spanners
from abjad.helpers.is_dominant_spanner import _is_dominant_spanner


## TODO: Deprecate entirely in favor of get_dominant_spanners_receipt( ).
##       After deprecation, rename get_dominant_spanners_receipt( )
##       to simply get_dominant_spanners.

def get_dominant_spanners(components):
   '''Return list of all spanners that include all components in list.'''
   
   # check input
   assert_components(components, contiguity = 'strict', share = 'thread')

   # get attached spanners
   attached_spanners = get_attached_spanners(components)

   # get dominant spanners
   dominant_spanners = [
      x for x in attached_spanners if _is_dominant_spanner(x, components)]

   # return dominant spanners
   return set(dominant_spanners)
