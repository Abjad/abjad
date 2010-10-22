from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface
from abjad.tools.formattools._get_comment_format_contributions_for_slot import \
   _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import \
   _get_context_mark_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import \
   _get_context_setting_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import \
   _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.formattools._get_grob_override_format_contributions import \
   _get_grob_override_format_contributions


class _ContextFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      formatter = self.formatter
      context = formatter.context
      if self._client._client.is_parallel:
         brackets_open = ['<<']
      else:
         brackets_open = ['{']
      engraver_removals = formatter._formatted_engraver_removals
      engraver_consists = formatter._formatted_engraver_consists
      overrides = _get_grob_override_format_contributions(self._client._client)
      settings = _get_context_setting_format_contributions(self._client._client)
      if engraver_removals or engraver_consists or overrides or settings:
         contributions = [formatter._invocation + r' \with {']
         result.append([('context_brackets', 'open'), contributions])
         contributions = ['\t' + x for x in engraver_removals]
         result.append([(formatter, 'engraver_removals'), contributions])
         contributions = ['\t' + x for x in engraver_consists]
         result.append([(formatter, 'engraver_consists'), contributions])
         contributions = ['\t' + x for x in overrides]
         result.append([('overrides', 'overrides'), contributions])
         contributions = ['\t' + x for x in settings] 
         result.append([('settings', 'settings'), contributions])
         contributions = ['} %s' % brackets_open[0]]
         result.append([('context_brackets', 'open'), contributions])
      else:
         contributions = [formatter._invocation + ' %s' % brackets_open[0]]
         result.append([('context_brackets', 'open'), contributions])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      context = self.formatter.context
      result.append([('comment_marks', ''),
         _get_comment_format_contributions_for_slot(context, 'opening')])
      result.append([('context_marks', 'context_marks'),
         _get_context_mark_format_contributions_for_slot(context, 'opening')])
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(context, 'opening')])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      context = self.formatter.context
      result.append([('context_marks', 'context_marks'),
         _get_context_mark_format_contributions_for_slot(context, 'closing')])
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(context, 'closing')])
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(context, 'closing')])
      self._indent_slot_contributions(result)
      return tuple(result)
