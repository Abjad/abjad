from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def component_is_orphan(component):
   '''``True`` when component has no parent, otherwise ``False``.
   
   ::

      abjad> note = Note(0, (1, 4))
      abjad> note._parentage.is_orphan
      True
   '''

   #return len(self.proper_parentage) == 0
   return not get_proper_parentage_of_component(component)
