from .. core.interface import _Interface

class TempoInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'MetronomeMark', ['Tempo'])
