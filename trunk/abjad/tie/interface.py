from .. core.interface import _Interface

class _TieInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Tie', ['Tie'] )
      self._set = None

   ### OVERRIDES ###

   def __nonzero__(self):
      return bool(self._set)

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   ### METHODS ###

   def clear(self):
      self._set = None
      _Interface.clear(self)

   def isTied(self):
      if (self._client.tie or self._client.tie.spanner) or\
         (self._client.prev and self._client.prev.tie):
         return True
      else:
         return False


   ### FORMATTING ###

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'~')
      return result
