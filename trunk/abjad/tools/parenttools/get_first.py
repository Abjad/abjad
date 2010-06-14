def get_first(component, klass):
   '''.. versionadded:: 1.1.1

   Return first instance of `klass` in parentage of `component`. ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> parenttools.get_first(staff[0], Staff)
      Staff{4}

   Otherwise return ``None``.
   '''

   for parent in component.parentage.parentage[1:]:
      if isinstance(parent, klass):
         return parent
