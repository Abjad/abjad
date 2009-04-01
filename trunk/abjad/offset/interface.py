from abjad.core.interface import _Interface
from abjad.rational.rational import Rational


class _OffsetInterface(_Interface):

   def __init__(self, _client, updateInterface):
      _Interface.__init__(self, _client)
      self._score = Rational(0)
      self._thread = Rational(0)
      updateInterface._observers.append(self)

   ## PRIVATE METHODS ##

   def _update(self):
      self._updateThread( )
      self._updateScore( )

   def _updateScore(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      if prev:
         offset += prev.offset.score + prev.duration.prolated
      self._score = offset

   def _updateThread(self):
      from abjad.helpers.assess_components import assess_components
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      if prev and assess_components([prev, self._client], 
         'strict', 'thread', False):
         offset += prev.offset.thread + prev.duration.prolated
      self._thread = offset

   ## PUBLIC ATTRIBUTES ##

   @property
   def score(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._score

   @property
   def thread(self):
      if not self._client._update._currentToRoot:
         self._client._update._updateAll( )
      return self._thread
