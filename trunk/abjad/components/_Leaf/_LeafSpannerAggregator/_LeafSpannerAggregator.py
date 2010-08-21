from abjad.components._Component._ComponentSpannerAggregator import _ComponentSpannerAggregator
from abjad.interfaces._Interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _after(self):
      from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
      from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
      from abjad.tools.lilyfiletools._make_lilypond_revert_string import \
         _make_lilypond_revert_string
      from abjad.tools import spannertools
      result = [ ]
      leaf = self._client
      #for spanner in self._spanners_in_parentage:
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
            spanner_contributions.extend(
               spanner.misc._get_formatted_commands_for_target_slot('closing'))
            spanner_contributions.extend(
               spanner.misc._get_formatted_commands_for_target_slot('after'))
         result.extend(spanner_contributions)
      return result

   ## TODO: OPTIMIZE!
   ##       Can take 16,678 function calls for a leaf in a single
   ##       staff with 100 leaves and a single spanner.
   @property
   def _before(self):
      from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
      from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
      from abjad.tools.lilyfiletools._make_lilypond_override_string import \
         _make_lilypond_override_string
      from abjad.tools import spannertools
      result = [ ]
      leaf = self._client
      #for spanner in self._spanners_in_parentage:
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

   @property
   def _left(self):
      from abjad.tools import spannertools
      result = [ ]
      leaf = self._client
      #for spanner in self._spanners_in_parentage:
      spanners = spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(leaf)
      spanners = list(spanners)
      spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
      for spanner in spanners:
         result.extend(spanner._format._left(leaf))   
      return result

   @property
   def _right(self):
      '''Order first by alphabetically by spanner class name;
      order next by stop / start status of spanner rel to leaf.
      '''
      from abjad.tools import spannertools
      stop_contributions = [ ]
      other_contributions = [ ]
      leaf = self._client
      #for spanner in self._spanners_in_parentage:
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
