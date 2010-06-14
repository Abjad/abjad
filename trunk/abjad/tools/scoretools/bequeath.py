from abjad.tools import parenttools
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to
from abjad.tools.spannertools.withdraw_from_crossing import \
   _withdraw_from_crossing


def bequeath(donors, recipients):
   '''Give everything from donors to recipients.
      Almost exactly the same as container setitem logic.
      This helper works with orphan donors.
      Container setitem logic can not work with orphan donors.
      Return donors.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(donors)
   assert componenttools.all_are_contiguous_components_in_same_parent(recipients)

   if len(donors) == 0:
      return donors

   parent, start, stop = parenttools.get_with_indices(donors)
   if parent:
      parent[start:stop+1] = recipients
      return donors
   else:
      _give_dominant_to(donors, recipients)
      _withdraw_from_crossing(donors)

   return donors
