from abjad.tools.componenttools.get_improper_parentage_of_component import \
   get_improper_parentage_of_component


def component_to_score_root(component):
   '''.. versionadded:: 1.1.1

   Get score root of `component`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> componenttools.component_to_score_root(note)
      Staff{1}

   Return score root.
   '''

   return get_improper_parentage_of_component(component)[-1]
