from abjad.interfaces._Interface import _Interface


class _ObserverInterface(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      updateInterface._observers.append(self)

   ## PRIVATE METHODS ##

   def _make_subject_update_if_necessary(self):
      try:
         observerSubject = self._client._update
      except AttributeError:
         ## t.offset.prolated
         observerSubject = self._client._client._update
      if not observerSubject._current_to_root:
         if True:
            observerSubject._update_all( )
