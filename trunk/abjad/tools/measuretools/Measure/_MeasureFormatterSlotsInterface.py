from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface
from abjad.tools.formattools._get_comment_format_contributions_for_slot import _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import _get_context_mark_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import _get_context_setting_format_contributions
from abjad.tools.formattools._get_grob_override_format_contributions import _get_grob_override_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import _get_lilypond_command_mark_format_contributions_for_slot


class _MeasureFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_3(self):
      r'''This is the slot where LilyPond grob \override commands live.
      This is also the slot where LilyPond \time commands live.
      '''
      result = [ ]
      measure = self.formatter.container
      result.append([('comment_marks', ''), 
         _get_comment_format_contributions_for_slot(measure, 'opening')])
      result.append([('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)])
      result.append([('settings', 'settings'),
         _get_context_setting_format_contributions(measure)])
      result.append([('context_marks', 'context_marks'),
         _get_context_mark_format_contributions_for_slot(measure, 'opening')])
      self._indent_slot_contributions(result)
      return tuple(result)
