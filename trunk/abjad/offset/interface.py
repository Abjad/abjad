from abjad.core.observer import _Observer
from abjad.rational.rational import Rational


class _OffsetInterface(_Observer):
   '''Serve rational rhythmic offset values.
      Handle no LilyPond grob.'''

   def __init__(self, _client, updateInterface):
      '''Bind to client and observer
         Set score and thread offsets to Rational(0).'''
      _Observer.__init__(self, _client, updateInterface)
      self._score = Rational(0)
      self._thread = Rational(0)

   ## PRIVATE METHODS ##

   def _update(self):
      self._updateThread( )
      self._updateScore( )

   def _updateScore(self):
      offset = Rational(0, 1)
      prev = self.client._navigator._prev
      if prev:
         offset += prev.offset.score + prev.duration.prolated
      self._score = offset

   def _updateThread(self):
      from abjad.tools import check
      offset = Rational(0, 1)
      prev = self.client._navigator._prev
      if prev and check.assess_components([prev, self.client], 
         contiguity = 'strict', share = 'thread', allow_orphans = False):
         offset += prev.offset.thread + prev.duration.prolated
      self._thread = offset

   ## PUBLIC ATTRIBUTES ##

   @property
   def score(self):
      '''Rational-valued rhythmic offset from beginning of score.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._score

   @property
   def thread(self):
      '''Rational-valued rhythmic offset from beginning of thread.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._thread
