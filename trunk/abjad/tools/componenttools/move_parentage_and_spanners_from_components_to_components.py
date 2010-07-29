from abjad.tools.spannertools.give_dominant_to import _give_dominant_to
from abjad.tools.spannertools.withdraw_from_crossing import _withdraw_from_crossing


def move_parentage_and_spanners_from_components_to_components(donors, recipients):
   '''Give everything from donors to recipients.
      Almost exactly the same as container setitem logic.
      This helper works with orphan donors.
      Container setitem logic can not work with orphan donors.
      Return donors.

   .. versionchanged:: 1.1.2
      renamed ``scoretools.bequeath( )`` to
      ``componenttools.move_parentage_and_spanners_from_components_to_components( )``.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.move_parentage_children_and_spanners_from_components_to_components( )`` to
      ``componenttools.move_parentage_and_spanners_from_components_to_components( )``.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(donors)
   assert componenttools.all_are_contiguous_components_in_same_parent(recipients)

   if len(donors) == 0:
      return donors

   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(donors)
   if parent:
      parent[start:stop+1] = recipients
      return donors
   else:
      _give_dominant_to(donors, recipients)
      _withdraw_from_crossing(donors)

   return donors
