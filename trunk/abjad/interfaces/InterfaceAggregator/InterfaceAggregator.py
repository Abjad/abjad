from abjad.interfaces._Interface import _Interface


class InterfaceAggregator(_Interface):
   '''Aggregate information about all format-contributing interfaces.
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      from abjad.tools.formattools._get_after_slot_format_contributions import \
         _get_after_slot_format_contributions
      return _get_after_slot_format_contributions(self._client)

   @property
   def before(self):
      from abjad.tools.formattools._get_before_slot_format_contributions import \
         _get_before_slot_format_contributions
      return _get_before_slot_format_contributions(self._client)

   @property
   def closing(self):
      from abjad.tools.formattools._get_closing_slot_format_contributions import \
         _get_closing_slot_format_contributions
      return _get_closing_slot_format_contributions(self._client)

   @property
   def left(self):
      from abjad.tools.formattools._get_left_slot_format_contributions import \
         _get_left_slot_format_contributions
      return _get_left_slot_format_contributions(self._client)

   @property
   def opening(self):
      from abjad.tools.formattools._get_opening_slot_format_contributions import \
         _get_opening_slot_format_contributions
      return _get_opening_slot_format_contributions(self._client)

   @property
   def overrides(self):
      from abjad.tools.formattools._get_grob_override_format_contributions import \
         _get_grob_override_format_contributions
      return _get_grob_override_format_contributions(self._client)

   @property
   def reverts(self):
      from abjad.tools.formattools._get_grob_revert_format_contributions import \
         _get_grob_revert_format_contributions
      return _get_grob_revert_format_contributions(self._client)

   @property
   def right(self):
      from abjad.tools.formattools._get_right_slot_format_contributions import \
         _get_right_slot_format_contributions
      return _get_right_slot_format_contributions(self._client)

   @property
   def settings(self):
      from abjad.tools.formattools._get_context_setting_format_contributions import \
         _get_context_setting_format_contributions
      return _get_context_setting_format_contributions(self._client)
