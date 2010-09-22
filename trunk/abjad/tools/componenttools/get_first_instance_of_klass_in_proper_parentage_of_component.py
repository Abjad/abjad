from abjad.tools.componenttools.get_proper_parentage_of_component import \
   get_proper_parentage_of_component


def get_first_instance_of_klass_in_proper_parentage_of_component(component, klass):
   '''.. versionadded:: 1.1.1

   Return first instance of `klass` in parentage of `component`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(staff[0], Staff)
      Staff{4}

   Otherwise return ``None``.

   .. todo:: implement corresponding function for improper parentage.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_first( )`` to
      ``componenttools.get_first_instance_of_klass_in_proper_parentage_of_component( )``.
   '''

   #for parent in component.parentage.proper_parentage:
   for parent in get_proper_parentage_of_component(component):
      if isinstance(parent, klass):
         return parent
