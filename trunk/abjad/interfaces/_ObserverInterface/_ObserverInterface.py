from abjad.interfaces._Interface import _Interface


class _ObserverInterface(_Interface):

   __slots__ = ( )

   def __init__(self, _client, update_interface):
      _Interface.__init__(self, _client)
      update_interface._observers.add(self)

   ## PRIVATE METHODS ##

   def _update_observer_interfaces_of_all_score_components_if_necessary(self):
      #print 'checking whether observer update is necessary ...'
      update_interface = self._client._update
      if update_interface._any_improper_parents_are_currently_updating:
         return
      if not update_interface._all_improper_parents_are_current:
         update_interface._update_observer_interfaces_of_all_score_components( )

   def _update_prolated_offset_values_of_all_score_components_if_necessary(self):
      update_interface = self._client._update
      if not update_interface._prolated_offset_values_of_all_improper_parents_are_current:
         update_interface._update_prolated_offset_values_of_all_score_components( )
