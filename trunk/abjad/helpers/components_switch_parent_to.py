from abjad.helpers.assert_components import assert_components


def _components_switch_parent_to(components, parent):
   '''NOT composer-safe.
      Helper assigns parent to component.
      Some other action should happen immediately afterwards.
      Because it's still necessary to assign components to parent.'''

   assert_components(components, contiguity = 'thread')

   for component in components:
      component.parentage._switchParentTo(parent)

   return components
