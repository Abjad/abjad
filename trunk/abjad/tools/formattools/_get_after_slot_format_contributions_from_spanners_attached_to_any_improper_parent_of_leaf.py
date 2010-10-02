def _get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   from abjad.tools import spannertools
   result = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      spanner_contributions = [ ]
      spanner_contributions.extend(spanner._format._after(leaf))
      if spanner._is_my_last_leaf(leaf):
         contributions = spanner.override._list_format_contributions('revert')
         spanner_contributions.extend(contributions)
      result.extend(spanner_contributions)
   return result
