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

   def _updateContext(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      self_parentage = self._client.parentage._threadParentage
      if prev and prev.parentage._threadParentage == self_parentage:
         offset += prev.offset.context + prev.duration.prolated
      self._context = offset

   def _updateScore(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      if prev:
         offset += prev.offset.score + prev.duration.prolated
      self._score = offset
