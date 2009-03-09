from abjad.core.interface import _Interface
from abjad.rational.rational import Rational


class _OffsetInterface(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      self._score = Rational(0)
      self._context = Rational(0)
      updateInterface._observers.append(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def context(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._context

   @property
   def score(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._score

   ## OBSERVER PATTERN INTERFACE ##

   ## TODO: Should this method be private?
   def update(self):
      self._updateContext( )
      self._updateScore( )

   ## TODO: these work fine now, but the method for computing the offset
   ## seems suboptimal. For one, Parengate._threadParentage might deprecate. 
   ## TODO: Wouldn't this method be better implemented by finding the
   ##       'root' of the context in which self._client lives,
   ##       and then performing a single depth-first search (using _DFS)
   ##       to visit each node-in-context only once?
   def _updateContext(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      self_parentage = self._client.parentage._threadParentage
      while prev and prev.parentage._threadParentage == self_parentage:
         offset += prev.duration.prolated
         prev = prev._navigator._prev
      self._context = offset

   ## TODO: See comment above about using depth-first search.
   def _updateScore(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      while prev:
         offset += prev.duration.prolated
         prev = prev._navigator._prev
      self._score = offset
