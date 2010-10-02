from abjad.components._Component._ComponentFormatterSlotsInterface import \
   _ComponentFormatterSlotsInterface
#from abjad.tools.formattools._get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
#   _get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
#from abjad.tools.formattools._get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
#   _get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
from abjad.tools.formattools._get_comment_format_contributions_for_slot import \
   _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import \
   _get_context_setting_format_contributions
from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import \
   _get_context_mark_format_contributions_for_slot
from abjad.tools.formattools._get_grob_override_format_contributions import \
   _get_grob_override_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import \
   _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.formattools._get_spanner_format_contributions_for_leaf_slot import \
   _get_spanner_format_contributions_for_leaf_slot


class _LeafFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   __slots__ = ( )

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      formatter = self.formatter
      leaf = formatter.leaf
      result = [ ]
      result.append(self.wrap(formatter, '_grace_body'))
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(leaf, 'before')])
      result.append([('lilypond_command_marks', ''), 
         _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'before')])
      result.append([('marks', 'marks'),
         _get_context_mark_format_contributions_for_slot(self._client._client, 'before')])
      result.append([('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)])
      result.append([('settings', 'settings'),
         _get_context_setting_format_contributions(self._client._client)])
      #result.append([(leaf.spanners, '_before'),
      #_get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      #leaf)])
      result.append([('spanners', 'before'),
         _get_spanner_format_contributions_for_leaf_slot(leaf, 'before')])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(leaf, 'opening')])
      result.append([('lilypond_command_marks', ''), 
         _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'opening')])
      result.append([('marks', 'marks'),
         _get_context_mark_format_contributions_for_slot(self._client._client, 'opening')])
      result.append(self.wrap(formatter, '_agrace_opening'))
      return tuple(result)

   @property
   def slot_4(self):
      result = [ ]
      result.append(self.wrap(self.formatter, '_leaf_body'))
      result.append(self._wrap_preceding_measure_bar_line_reverts( ))
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(formatter, '_agrace_body'))
      result.append([('lilypond_command_marks', ''), 
         _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'closing')])
      result.append([('marks', 'marks'),
         _get_context_mark_format_contributions_for_slot(self._client._client, 'closing')])
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(leaf, 'closing')])
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      #result.append([(leaf.spanners, '_after'),
      #_get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      #leaf)])
      result.append([('spanners', ''), 
         _get_spanner_format_contributions_for_leaf_slot(leaf, 'after')])
      result.append([('marks', 'marks'),
         _get_context_mark_format_contributions_for_slot(leaf, 'after')])
      result.append([('lilypond_command_marks', ''), 
         _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'after')])
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(leaf, 'after')])
      return tuple(result)

   ## PRIVATE METHODS ##

   ## FIXME: make work with new grob override pattern ##
   def _wrap_preceding_measure_bar_line_reverts(self):
      from abjad.components import Measure
      from abjad.tools import componenttools
      from abjad.tools import measuretools
      leaf = self.formatter._client
      containing_measure = componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(leaf, Measure)
      if containing_measure is None:
         return [('Special', 'reverts'), [ ]]
      if leaf is not containing_measure.leaves[0]:
         return [('Special', 'reverts'), [ ]]
      prev_measure = measuretools.get_prev_measure_from_component(containing_measure)
      if prev_measure is None:
         return [('Special', 'reverts'), [ ]]
      bar_line_reverts = [ ]
      ## FIXME
      #bar_line_reverts.extend(prev_measure.override.bar_line._reverts)
      #bar_line_reverts.extend(prev_measure.override.span_bar._reverts)
      return [('Special', 'reverts'), bar_line_reverts]
