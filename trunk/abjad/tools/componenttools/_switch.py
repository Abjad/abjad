def _switch(components, parent):
   '''NOT composer-safe.
   Helper assigns parent to component.
   Some other action should happen immediately afterwards.
   Because it's still necessary to assign components to parent.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_thread_contiguous_components(components)

   for component in components:
      component.parentage._switch(parent)

   return components
