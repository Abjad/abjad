from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners
from abjad.helpers.components_fracture_shallow import \
   components_fracture_shallow


def components_fracture_unspan(component_list):
   '''Fracture to the left of leftmost component at top level of list.
      fracture to the right of rightmost component at top level of list.
      Unspan all components at top level of list.
      Return component_list.'''

   # fracture to the left and right of first and last components at top level
   components_fracture_shallow(component_list)

   # unspan all components at top level of list
   _withdraw_from_attached_spanners(component_list)
   
   # return input list
   return component_list
