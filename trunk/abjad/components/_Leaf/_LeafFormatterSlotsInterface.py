from abjad.components._Component._ComponentFormatterSlotsInterface import _ComponentFormatterSlotsInterface


class _LeafFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      from abjad.tools.formattools._get_grob_override_format_contributions import \
         _get_grob_override_format_contributions
      from abjad.tools.formattools._get_context_setting_format_contributions import \
         _get_context_setting_format_contributions
      from abjad.tools.formattools._get_before_slot_format_contributions import \
         _get_before_slot_format_contributions
      from abjad.tools.leaftools._get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
      _get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(formatter, '_grace_body'))
      result.append(self.wrap(leaf.comments, 'before'))
      result.append(self.wrap(leaf.directives, 'before'))

      #result.append(self.wrap(leaf.interfaces, 'overrides'))
      #result.append(self.wrap(leaf.interfaces, 'settings'))

      result.append([('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)])
      result.append([('settings', 'settings'),
         _get_context_setting_format_contributions(self._client._client)])

      #result.append(self.wrap(leaf.spanners, '_before'))
      ## wrap format contributions by hand:
      result.append([(leaf.spanners, '_before'),
      _get_before_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      leaf)])

      #result.append(self.wrap(leaf.interfaces, 'before'))
      result.append([('before', 'before'),
         _get_before_slot_format_contributions(self._client._client)])

      return tuple(result)

   @property
   def slot_3(self):
      from abjad.tools.formattools._get_opening_slot_format_contributions import \
         _get_opening_slot_format_contributions
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(leaf.comments, 'opening'))
      result.append(self.wrap(leaf.directives, 'opening'))

      #result.append(self.wrap(leaf.interfaces, 'opening'))
      result.append([('opening', 'opening'),
         _get_opening_slot_format_contributions(self._client._client)])

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
      from abjad.tools.formattools._get_closing_slot_format_contributions import \
         _get_closing_slot_format_contributions
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(formatter, '_agrace_body'))
      result.append(self.wrap(leaf.directives, 'closing'))

      #result.append(self.wrap(leaf.interfaces, 'closing'))
      result.append([('closing', 'closing'),
         _get_closing_slot_format_contributions(self._client._client)])

      result.append(self.wrap(leaf.comments, 'closing'))
      return tuple(result)

   @property
   def slot_7(self):
      from abjad.tools.formattools._get_after_slot_format_contributions import \
         _get_after_slot_format_contributions
      from abjad.tools.leaftools._get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf import \
      _get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf

      #result.append(self.wrap(leaf.interfaces, 'after'))
      result.append([('after', 'after'),
         _get_after_slot_format_contributions(self._client._client)])

      #result.append(self.wrap(leaf.spanners, '_after'))
      result.append([(leaf.spanners, '_after'),
      _get_after_slot_format_contributions_from_spanners_attached_to_any_improper_parent_of_leaf(
      leaf)])

      result.append(self.wrap(leaf.directives, 'after'))
      result.append(self.wrap(leaf.comments, 'after'))
      return tuple(result)

   ## PRIVATE METHODS ##

   ## FIXME: make work with new grob override pattern ##
   def _wrap_preceding_measure_bar_line_reverts(self):
      from abjad.components.Measure import _Measure
      from abjad.tools import componenttools
      from abjad.tools import measuretools
      leaf = self.formatter._client
      containing_measure = componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(leaf, _Measure)
      if containing_measure is None:
         return [('Special', 'reverts'), [ ]]
      if leaf is not containing_measure.leaves[0]:
         return [('Special', 'reverts'), [ ]]
      prev_measure = measuretools.get_prev_measure_from_component(containing_measure)
      if prev_measure is None:
         return [('Special', 'reverts'), [ ]]
      bar_line_reverts = [ ]
      #bar_line_reverts.extend(prev_measure.bar_line._reverts)
      #bar_line_reverts.extend(prev_measure.span_bar._reverts)
      ## FIXME
      #bar_line_reverts.extend(prev_measure.override.bar_line._reverts)
      #bar_line_reverts.extend(prev_measure.override.span_bar._reverts)
      return [('Special', 'reverts'), bar_line_reverts]
