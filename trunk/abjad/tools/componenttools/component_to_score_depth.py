from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def component_to_score_depth(component):
   '''Get the nonnegative integer number of components in the proper parentage of `component`:

   ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> note.parentage.depth
      2
   '''

   return len(get_proper_parentage_of_component(component))
