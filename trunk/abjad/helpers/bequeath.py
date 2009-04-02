from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.give_dominant_spanners_to import \
   _give_dominant_spanners_to
from abjad.helpers.withdraw_from_crossing_spanners import \
   _withdraw_from_crossing_spanners


def bequeath(donors, recipients):
   '''Give everything from donors to recipients.
      Almost exactly the same as container setitem logic.
      This helper works with orphan donors.
      Container setitem logic can not work with orphan donors.
      Return donors.'''

   assert_components(donors, contiguity = 'strict', share = 'parent')
   assert_components(recipients, contiguity = 'strict', share = 'parent')

   if len(donors) == 0:
      return donors

   parent, start, stop = get_parent_and_indices(donors)
   if parent:
      parent[start:stop+1] = recipients
      return donors
   else:
      _give_dominant_spanners_to(donors, recipients)
      _withdraw_from_crossing_spanners(donors)

   return donors
