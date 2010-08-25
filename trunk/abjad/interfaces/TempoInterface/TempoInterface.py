from abjad.interfaces._Interface import _Interface


class TempoInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_tempo import get_effective_tempo
      return get_effective_tempo(self._client)
