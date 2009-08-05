from abjad.tools import check


def _cut(components):
   '''Cut all components in list from parent.
      Does not handle spanners and so not composer-safe.'''

   check.assert_components(components)

   for component in components:
      component.parentage._cut( )

   return components
