from abjad.helpers.fracture_attached_spanners import \
   fracture_attached_spanners
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners


def components_fracture_unspan(components):
   '''Fracture to the left of leftmost component at top level of list.
      fracture to the right of rightmost component at top level of list.
      Unspan all components at top level of list.
      Return components.'''

   ## fracture to the left and right of first and last components at top level
   fracture_attached_spanners(components)

   ## unspan all components at top level of list
   _withdraw_from_attached_spanners(components)
   
   ## return components
   return components
