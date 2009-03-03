from abjad.helpers.are_contiguous_components import _are_contiguous_components
from abjad.helpers.are_orphan_components import _are_orphan_components


def _are_successive_components(ll):
   '''Return True when ll is a Python list and when either
   each of the elements in ll is an orphan Abjad component or when
   all elements in ll share the same (container) parent,
   otherwise False.

   Intended for type-checking helper function input.
   Generalization of _are_contiguous_components, _are_orphan_components.

   NOTE: 

   Helper functions that handle only *containerized* components
   should assert _are_contiguous_components.

   Helper functions that handle both containerized components AND
   also components in a built-in Python list (say a Python list of
   measures prior to staff insertion) should instead assert
   _are_successive_components.

   (So _are_successive_components is more lenient than 
   _are_contiguous_components.)'''
   
   return _are_contiguous_components(ll) or _are_orphan_components(ll)
