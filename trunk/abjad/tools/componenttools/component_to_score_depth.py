from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def component_to_score_depth(component):
   '''Get score depth of `component`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> componenttools.component_to_score_depth(staff.leaves[0])
      2

   Return nonnegative integer.
   '''

   return len(get_proper_parentage_of_component(component))
