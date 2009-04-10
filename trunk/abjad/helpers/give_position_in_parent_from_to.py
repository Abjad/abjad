from abjad.helpers.assert_components import assert_components
from abjad.tools import parenttools


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

   parent, start, stop = parenttools.get_with_indices(donors)

   if parent is None:
      return donors

   parent._music[start:start] = recipients
   parenttools.switch(recipients, parent)
   parenttools.switch(donors, None)

   return donors
