from abjad.cfg.session import _CFG
from abjad.interfaces.interface.interface import _Interface


class _Observer(_Interface):

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
         if getattr(_CFG, 'update', True):
            observerSubject._update_all( )
