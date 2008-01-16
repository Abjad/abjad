from .. core.interface import _Interface

class TempoInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'Tempo')

   ### SPANNER-DERIVED PROPERTIES ###

   @property
   def tempo(self):
      return self._client.spanners.getValue('TempoInterface', 'tempo')
