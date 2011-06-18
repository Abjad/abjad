from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface
from abjad.tools.formattools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import _get_context_mark_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import _get_context_setting_format_contributions
from abjad.tools.formattools._get_grob_override_format_contributions import _get_grob_override_format_contributions
from abjad.tools.formattools._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot


class _MeasureFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      '''Optional start-of-measure numbering indicator. Open bracket.
      '''
      result = [ ]
      formatter = self._client
      measure = formatter._client
## FIXME ##
#      contribution = formatter.number._measure_contribution
#      if contribution == 'comment':
#         contributor = (formatter.number, '_measure_contribution')
#         contributions = ['%% start measure %s' % measure.number]
#         result.append([contributor, contributions])
      brackets = _ContainerFormatterSlotsInterface.slot_2.fget(self) 
      result.extend(brackets)
      return tuple(result)

   @property
   def slot_3(self):
      r'''This is the slot where LilyPond grob \override commands live.
      Measure need to override the default container behavior for slot 3
      assembly in order to push bar_line overrides to slot 5, later in
      the format string. Otherwise, measure contents of slot 3 is just
      like generic container contents of slot 3.
      '''
      result = [ ]
      measure = self.formatter.container
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(measure, 'opening')])
      result.append(self._wrap_measure_interface_overrides( ))
      result.append([('settings', 'settings'),
         _get_context_setting_format_contributions(measure)])
      result.append([('context_marks', 'context_marks'),
         _get_context_mark_format_contributions_for_slot(measure, 'opening')])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      r'''Just like container slot 5. But with any LilyPond BarLine
      \override strings included FIRST THING so as to appear PRIOR TO
      any LilyPond BarLine \revert strings that may appear later.
      '''
      result = [ ]
      measure = self.formatter.container
      result.append(self._wrap_bar_line_interface_overrides( ))
      result.append(self._wrap_measure_interface_reverts( ))
      result.append([('context_marks', 'context_marks'),
         _get_context_mark_format_contributions_for_slot(measure, 'closing')])
      result.append([('comment_marks', ''),
         _get_comment_format_contributions_for_slot(measure, 'closing')])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      '''Close bracket. Optional end-of-measure numbering indicator.
      '''
      result = [ ]
      formatter = self._client
      measure = formatter._client
      brackets = _ContainerFormatterSlotsInterface.slot_6.fget(self)
      result.extend(brackets)
## FIXME ##
#      contribution = formatter.number._measure_contribution
#      if contribution == 'comment':
#         contributor = (formatter.number, '_measure_contribution')
#         contributions = ['%% stop measure %s' % measure.number]
#         result.append([contributor, contributions])
      return tuple(result)

   ## PRIVATE METHODS ##

   ## FIXME: make work with new grob override pattern ##
   def _wrap_bar_line_interface_overrides(self):
      measure = self.formatter.container
      bar_line_overrides = [ ]
      ## FIXME ##
      #bar_line_overrides.extend(measure.override.bar_line._overrides)
      #bar_line_overrides.extend(measure.override.span_bar._overrides)
      return [('BarLine / SpanBar', 'overrides'), bar_line_overrides]
      
   def _wrap_measure_interface_overrides(self):
      '''To allow filtering out of BarLine overrides.'''
      result = [('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)]
      override_list = result[-1]
      override_list = [x for x in override_list if 'BarLine' not in x and 'SpanBar' not in x]
      result[-1] = override_list
      return result

   def _wrap_measure_interface_reverts(self):
      '''To allow filtering out of BarLine reverts.
      '''
      result = [('reverts', 'reverts'),
         _get_grob_revert_format_contributions(self._client._client)]
      override_list = result[-1]
      override_list = [x for x in override_list if 'BarLine' not in x and 'SpanBar' not in x]
      result[-1] = override_list
      return result
