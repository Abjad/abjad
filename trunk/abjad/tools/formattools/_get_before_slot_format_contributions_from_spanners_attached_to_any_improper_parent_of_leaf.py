def _get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   from abjad.tools import spannertools
   result = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      spanner_contributions = [ ]
      if spanner._is_my_first_leaf(leaf):
         contributions = spanner.override._list_format_contributions('override', is_once = False)
         spanner_contributions.extend(contributions)
      spanner_contributions.extend(spanner._format._before(leaf))
      result.extend(spanner_contributions)
   return result
