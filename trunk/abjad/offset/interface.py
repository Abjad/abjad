from abjad.core.interface import _Interface
from abjad.rational.rational import Rational

class _OffsetInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)


   @property
   def context(self):
      prev = self._client._navigator._prev
      if prev and prev._parentage._threadParentage == \
            self._client._parentage._threadParentage:
         result = prev.offset.context + prev.duration.prolated 
      else:
         result = Rational(0, 1)
      return result         

   @property
   def score(self):
      prev = self._client._navigator._prev
      if prev:
         result = prev.offset.score + prev.duration.prolated 
      else:
         result = Rational(0, 1)
      return result
