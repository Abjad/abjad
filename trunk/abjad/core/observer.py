from abjad.cfg.session import _CFG
from abjad.core.interface import _Interface


class _Observer(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      updateInterface._observers.append(self)

   ## PRIVATE METHODS ##

   def _makeSubjectUpdateIfNecessary(self):
      try:
         observerSubject = self._client._update
      except AttributeError:
         ## t.offset.prolated
         observerSubject = self._client._client._update
      if not observerSubject._currentToRoot:
         if getattr(_CFG, 'update', True):
            observerSubject._updateAll( )
