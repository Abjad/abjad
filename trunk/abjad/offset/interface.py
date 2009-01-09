from abjad.core.interface import _Interface
from abjad.rational.rational import Rational


class _OffsetInterface(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      self._score = Rational(0)
      self._context = Rational(0)
      updateInterface._observers.append(self)


   ### PUBLIC PROPERTIES ###

   @property
   def score(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._score

   @property
   def context(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._context


   ### OBSERVER PATTERN INTERFACE ###

   def update(self):
      self._updateContext( )
      self._updateScore( )

   ### TODO: these work fine now, but the method for computing the offset
   ### seems suboptimal. For one, Parengate._threadParentage might deprecate. 
   def _updateContext(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      self_parentage = self._client._parentage._threadParentage
      while prev and prev._parentage._threadParentage == self_parentage:
         offset += prev.duration.prolated
         prev = prev._navigator._prev
      self._context = offset

   def _updateScore(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      while prev:
         offset += prev.duration.prolated
         prev = prev._navigator._prev
      self._score = offset
