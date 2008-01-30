from .. core.interface import _Interface

class _TrillInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'TrillSpanner', ['Trill'] )
      self._set = None
