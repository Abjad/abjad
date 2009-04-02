from abjad.helpers.assert_components import assert_components
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to
from abjad.helpers.get_parent_and_indices import get_parent_and_indices


def _give_position_in_parent_from_to(donors, recipients):
   '''When 'donors' has a parent, find parent.
      Then insert all components in 'recipients'
      in parent immediately before 'donors'.
      Then remove 'donors' from parent.

      When 'donors' has no parent, do nothing.

      Return 'donors'.

      Helper implements no spanner-handling at all.
      Helper is not composer-safe and may cause discontiguous spanners.'''

   assert_components(donors, contiguity = 'strict', share = 'parent')
   assert_components(recipients)

   parent, start, stop = get_parent_and_indices(donors)

   if parent is None:
      return donors

   parent._music[start:start] = recipients
   _components_switch_parent_to(recipients, parent)
   _components_switch_parent_to(donors, None)

   return donors
