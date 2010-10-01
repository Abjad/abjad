from abjad.components._Component._ComponentFormatterSlotsInterface import \
   _ComponentFormatterSlotsInterface
from abjad.tools.formattools._get_comment_contribution_for_slot import \
   _get_comment_contribution_for_slot
from abjad.tools.formattools._get_lilypond_command_mark_contribution_for_slot import \
   _get_lilypond_command_mark_contribution_for_slot
from abjad.tools.formattools._get_grob_override_format_contributions import \
   _get_grob_override_format_contributions
from abjad.tools.formattools._get_grob_revert_format_contributions import \
   _get_grob_revert_format_contributions
from abjad.tools.formattools._get_opening_slot_format_contributions import \
   _get_opening_slot_format_contributions
from abjad.tools.formattools._get_context_setting_format_contributions import \
   _get_context_setting_format_contributions
from abjad.tools.formattools._get_closing_slot_format_contributions import \
   _get_closing_slot_format_contributions


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
      result.append([('comment_marks', ''), 
         _get_comment_contribution_for_slot(container, 'before')])
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_contribution_for_slot(container, 'before')])
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      if self._client._client.parallel:
         brackets_open = ['<<']
      else:
         brackets_open = ['{']
      result.append([('container_brackets', 'open'), brackets_open])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      container = self.formatter.container
      result.append([('comment_marks', ''), 
         _get_comment_contribution_for_slot(container, 'opening')])
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_contribution_for_slot(container, 'opening')])
      result.append([('overrides', 'overrides'), 
         _get_grob_override_format_contributions(self._client._client)])
      result.append([('opening', 'opening'), 
         _get_opening_slot_format_contributions(self._client._client)])
      result.append([('settings', 'settings'), 
         _get_context_setting_format_contributions(self._client._client)])
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
      result.append([('closing', 'closing'), 
         _get_closing_slot_format_contributions(self._client._client)])
      result.append([('reverts', 'reverts'), 
         _get_grob_revert_format_contributions(self._client._client)])
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_contribution_for_slot(container, 'closing')])
      result.append([('comment_marks', ''), 
         _get_comment_contribution_for_slot(container, 'closing')])
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      if self._client._client.parallel:
         brackets_close = ['>>']
      else:
         brackets_close = ['}']
      result.append([('context_brackets', 'close'), brackets_close])
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      container = self.formatter.container
      result.append([('lilypond_command_marks', ''),
         _get_lilypond_command_mark_contribution_for_slot(container, 'after')])
      result.append([('comment_marks', ''), _get_comment_contribution_for_slot(container, 'after')])
      return tuple(result)

   ## PUBLIC METHODS ##

   def contributions(self, attr):
      result = [ ]
      for contributor, contributions in getattr(self, attr):
         result.extend(contributions)
      return result
