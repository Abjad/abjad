from abjad.tools.componenttools.get_improper_parentage_of_component import \
   get_improper_parentage_of_component


def get_proper_parentage_of_component(component):
   '''.. versionadded:: 1.1.1

   Get tuple of all components in parentage of `component`
   excluding `component`::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> note._parentage.proper_parentage
      (tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1})
   '''

   #return tuple(self.improper_parentage[1:])
   return get_improper_parentage_of_component(component)[1:]
