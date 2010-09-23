from abjad.tools.componenttools.get_improper_parentage_of_component import \
   get_improper_parentage_of_component


def component_to_score_root(component):
   '''Reference to root-level component in parentage 
   of `component`. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> note._parentage.root
      Staff{1}
   '''

   #return self.improper_parentage[-1]
   return get_improper_parentage_of_component(component)[-1]
