def _get_right_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   '''Order first by alphabetically by spanner class name;
   order next by stop / start status of spanner rel to leaf.
   '''
   from abjad.tools import spannertools
   stop_contributions = [ ]
   other_contributions = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      contributions = spanner._format._right(leaf)
      if contributions:
         if spanner._is_my_last_leaf(leaf):
            stop_contributions.extend(contributions)
         else:
            other_contributions.extend(contributions)
   result = stop_contributions + other_contributions
   return result
