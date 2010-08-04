def get_parent_and_start_stop_indices_of_components(components):
   r'''Return ``(parent, start, stop)`` triple with
   
   *  ``parent`` a reference to the parent of ``components``
   *  ``start`` the index of ``components[0]`` in ``parent``
   *  ``stop`` the index of ``components[-1]`` in ``parent``

   Any of the three return values may equal ``None``.

   ::

      abjad> t = Staff(macros.scale(6))
      abjad> print t.format
      \new Staff {
         c'8
         d'8
         e'8
         f'8
         g'8
         a'8
      }

   ::

      abjad> leaves = t[-2:]
      abjad> leaves
      [Note(g', 8), Note(a', 8)]
      abjad> componenttools.get_parent_and_start_stop_indices_of_components(leaves)
      (Staff{6}, 4, 5)

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_with_indices( )`` to
      ``componenttools.get_parent_and_start_stop_indices_of_components( )``.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_thread_contiguous_components(components)

   if len(components) > 0:
      first, last = components[0], components[-1]
      parent = first.parentage.parent
      if parent is not None:
         first_index = parent.index(first)
         last_index = parent.index(last)
         return parent, first_index, last_index

   return None, None, None
