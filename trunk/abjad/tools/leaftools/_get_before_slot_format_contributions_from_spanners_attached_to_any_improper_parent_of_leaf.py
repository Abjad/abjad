## TODO: OPTIMIZE!
##       Can take 16,678 function calls for a leaf in a single
##       staff with 100 leaves and a single spanner.
def _get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
   leaf):
   from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
   from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
   from abjad.tools.lilyfiletools._make_lilypond_override_string import \
      _make_lilypond_override_string
   from abjad.tools import spannertools
   result = [ ]
   spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
   spanners = list(spanners)
   spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
   for spanner in spanners:
      #result.extend(spanner._format._before(leaf))
      spanner_contributions = [ ]
      if spanner._is_my_first_leaf(leaf):
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
                     spanner_override_contributions.append(
                        _make_lilypond_override_string(grob_name, grob_attribute,
                        grob_value, context_name = context_name, is_once = False))
            elif isinstance(value, LilyPondGrobProxy):
               grob_name, grob_namespace = name, value
               for grob_attribute, grob_value in vars(grob_namespace).iteritems( ):
                  spanner_override_contributions.append(
                     _make_lilypond_override_string(grob_name, grob_attribute,
                     grob_value, is_once = False))
         spanner_override_contributions.sort( )
         spanner_contributions.extend(spanner_override_contributions)
         spanner_contributions.extend(
            spanner.misc._get_formatted_commands_for_target_slot('before'))
         spanner_contributions.extend(
            spanner.misc._get_formatted_commands_for_target_slot('opening'))
      spanner_contributions.extend(spanner._format._before(leaf))
      result.extend(spanner_contributions)
   return result
