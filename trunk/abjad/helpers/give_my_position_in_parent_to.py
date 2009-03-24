from abjad.helpers.assert_components import _assert_components
from abjad.helpers.get_parent_and_index import _get_parent_and_index
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to


def _give_my_position_in_parent_to(donor_component, recipient_components):
   '''When 'donor_component' has a parent, find parent.
      Then insert all components in 'recipient_components'
      in parent immediately before 'donor_component'.
      Then remove 'donor_component' from parent.

      When 'donor_component' has no parent, do nothing.

      Return 'donor_component'.

      Helper implements no spanner-handling at all.
      Helper is not composer-safe and may cause discontiguous spanners.'''

   _assert_components([donor_component])
   _assert_components(recipient_components)

   parent, index = _get_parent_and_index([donor_component])

   if parent is None:
      return donor_component

   parent._music[index:index] = recipient_components
   _components_switch_parent_to(recipient_components, parent)
   donor_component.parentage._switchParentTo(None)

   return donor_component
