from abjad.helpers.components_unspan_shallow import components_unspan_shallow
from abjad.helpers.components_fracture_around import components_fracture_around


def components_fracture_unspan(component_list):
   '''Fracture to the left of leftmost component in list;
      fracture to the right of rightmost component in list;
      unspan all components in list;
      return components in list.'''

   components_fracture_around(component_list)
   components_unspan_shallow(component_list)
   
   return component_list
