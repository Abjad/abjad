from abjad.interfaces._Interface import _Interface


class _ObserverInterface(_Interface):

   def __init__(self, _client, update_interface):
      _Interface.__init__(self, _client)
      update_interface._observers.add(self)

   ## PRIVATE METHODS ##

   def _make_subject_update_if_necessary(self):
      update_interface = self._client._update
      if not update_interface._all_improper_parents_are_current:
         update_interface._update_observer_interfaces_attached_to_all_score_components( )
