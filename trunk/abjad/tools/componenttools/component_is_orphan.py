from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def component_is_orphan(component):
   '''True when `component` has no parent. Otherwise false::

      abjad> note = Note(0, (1, 4))
      abjad> componenttools.component_is_orphan(note)
      True
   
   Return boolean.
   '''

   return not get_proper_parentage_of_component(component)
