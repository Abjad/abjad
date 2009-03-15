from abjad.helpers.components_detach_spanners_shallow import components_detach_spanners_shallow
from abjad.helpers.components_fracture_shallow import components_fracture_shallow


def components_fracture_unspan(component_list):
   '''Fracture to the left of leftmost component at top level of list.
      fracture to the right of rightmost component at top level of list.
      Unspan all components at top level of list.
      Return component_list.'''

   # fracture to the left and right of first and last components at top level
   components_fracture_shallow(component_list)

   # unspan all components at top level of list
   components_unspan_shallow(component_list)
   
   # return input list
   return component_list
