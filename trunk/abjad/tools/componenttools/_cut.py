def _cut(components):
   '''Cut all components in list from parent.
      Does not handle spanners and so not composer-safe.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_components(components)

   for component in components:
      component.parentage._cut( )

   return components
