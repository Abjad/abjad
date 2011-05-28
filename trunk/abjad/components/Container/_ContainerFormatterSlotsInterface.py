from abjad.components._Component._ComponentFormatterSlotsInterface import _ComponentFormatterSlotsInterface
from abjad.tools.formattools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import _get_context_setting_format_contributions
from abjad.tools.formattools._get_grob_override_format_contributions import _get_grob_override_format_contributions
from abjad.tools.formattools._get_grob_revert_format_contributions import _get_grob_revert_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot


class _ContainerFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)

   ## PRIVATE METHODS ##

   def _indent_slot_contributions(self, slot):
      for contributor, contributions in slot:
         if contributions:
            for i, contribution in enumerate(contributions):
               contributions[i] = '\t' + contribution
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      container = self.formatter.container
      result.append([('comments', ''), 
         _get_comment_format_contributions_for_slot(container, 'before')])
      result.append([('lilypond command marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(container, 'before')])
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      if self._client._client.is_parallel:
         brackets_open = ['<<']
      else:
         brackets_open = ['{']
      result.append([('open brackets', ''), brackets_open])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      container = self.formatter.container
      result.append([('comments', ''), 
         _get_comment_format_contributions_for_slot(container, 'opening')])
      result.append([('lilypond command marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(container, 'opening')])
      result.append([('grob overrides', ''), 
         _get_grob_override_format_contributions(container)])
      result.append([('context settings', ''), 
         _get_context_setting_format_contributions(container)])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_4(self):
      result = [ ]
      result.append(self.wrap(self.formatter, '_contents'))
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      container = self.formatter.container
      result.append([('grob reverts', ''), 
         _get_grob_revert_format_contributions(container)])
      result.append([('lilypond command marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(container, 'closing')])
      result.append([('comments', ''), 
         _get_comment_format_contributions_for_slot(container, 'closing')])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      if self._client._client.is_parallel:
         brackets_close = ['>>']
      else:
         brackets_close = ['}']
      result.append([('close brackets', ''), brackets_close])
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      container = self.formatter.container
      result.append([('lilypond command marks', ''),
         _get_lilypond_command_mark_format_contributions_for_slot(container, 'after')])
      result.append([('comments', ''), 
         _get_comment_format_contributions_for_slot(container, 'after')])
      return tuple(result)

   ## PUBLIC METHODS ##

   def contributions(self, attr):
      result = [ ]
      for contributor, contributions in getattr(self, attr):
         result.extend(contributions)
      return result
