from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def component_to_tuplet_depth(component):
   '''Nonnegative integer number of tuplets in the proper parentage 
   of `component`. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> note._parentage.depth_tuplet
      1

   Tuplets do not count as containing themselves. ::

      abjad> tuplet._parentage.depth_tuplet
      0

   Zero when there is no tuplet in the proper parentage of component. ::

      abjad> staff._parentage.depth_tuplet
      0
   '''
   from abjad.components.Tuplet import Tuplet

   result = 0
   for parent in get_proper_parentage_of_component(component):
      if isinstance(parent, Tuplet):
         result += 1
   return result
