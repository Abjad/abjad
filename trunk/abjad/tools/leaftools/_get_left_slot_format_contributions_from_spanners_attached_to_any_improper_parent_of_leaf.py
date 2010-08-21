def _get_left_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   from abjad.tools import spannertools
   result = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      result.extend(spanner._format._left(leaf))   
   return result
