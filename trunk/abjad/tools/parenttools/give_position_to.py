from abjad.helpers.assert_components import assert_components
from abjad.tools.parenttools.get_with_indices import get_with_indices
from abjad.tools.parenttools.switch import switch


def _give_position_to(donors, recipients):
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

   parent, start, stop = get_with_indices(donors)

   if parent is None:
      return donors

   parent._music[start:start] = recipients
   switch(recipients, parent)
   switch(donors, None)

   return donors
