def _get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
   from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
   from abjad.tools.lilyfiletools._make_lilypond_revert_string import \
      _make_lilypond_revert_string
   from abjad.tools import spannertools
   result = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      spanner_contributions = [ ]
      spanner_contributions.extend(spanner._format._after(leaf))
      if spanner._is_my_last_leaf(leaf):
         spanner_override_contributions = [ ]
         for name, value in vars(spanner.override).iteritems( ):
            #print name, value
            if isinstance(value, LilyPondGrobProxyContextWrapper):
               context_name, context_wrapper = name.lstrip('_'), value
               #print context_name, context_wrapper
               for grob_name, grob_override_namespace in vars(context_wrapper).iteritems( ):
                  #print grob_name, grob_override_namespace
                  for grob_attribute, grob_value in vars(grob_override_namespace).iteritems( ):
                     #print grob_attribute, grob_value
                     spanner_override_contributions.append(_make_lilypond_revert_string(
                        grob_name, grob_attribute, context_name = context_name))
            elif isinstance(value, LilyPondGrobProxy):
               grob_name, grob_namespace = name, value
               for grob_attribute, grob_value in vars(grob_namespace).iteritems( ):
                  spanner_override_contributions.append(
                     _make_lilypond_revert_string(grob_name, grob_attribute))
         spanner_override_contributions.sort( )
         spanner_contributions.extend(spanner_override_contributions)
#         spanner_contributions.extend(
#            spanner.misc._get_formatted_commands_for_target_slot('closing'))
#         spanner_contributions.extend(
#            spanner.misc._get_formatted_commands_for_target_slot('after'))
      result.extend(spanner_contributions)
   return result
