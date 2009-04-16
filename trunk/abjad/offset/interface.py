from abjad.core.observer import _Observer
from abjad.rational.rational import Rational


class _OffsetInterface(_Observer):
   '''Serve rational rhythmic offset values.
      Handle no LilyPond grob.'''

   def __init__(self, _client, updateInterface):
      '''Bind to client and register self as observer.
         Init score and thread offsets to zero.'''
      _Observer.__init__(self, _client, updateInterface)
      self._score = Rational(0)
      self._thread = Rational(0)

   ## PRIVATE METHODS ##

   def _update(self):
      '''Update offset values of any one node in score.'''
      self._updateThread( )
      self._updateScore( )

   def _updateScore(self):
      '''Update score offset of any one node in score.'''
      prev = self.client._navigator._prev
      if prev:
         self._score = prev.offset.score + prev.duration.prolated
      else:
         self._score = Rational(0)

   def _updateThread(self):
      '''Update thread offset of any one node in score.'''
      from abjad.tools import check
      prev = self.client._navigator._prev
      if prev and check.assess_components([prev, self.client], 
         contiguity = 'strict', share = 'thread', allow_orphans = False):
         self._thread = prev.offset.thread + prev.duration.prolated
      else:
         self._thread = Rational(0)

   ## PUBLIC ATTRIBUTES ##

   @property
   def score(self):
      '''Rational-valued rhythmic offset from beginning of score.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._score

   ## TODO: Possibly remove _OffsetInterface.thread? ##
   ## TODO: Possibly t.offset.start and t.offset.stop? ##

   @property
   def thread(self):
      '''Rational-valued rhythmic offset from beginning of thread.'''
      self._makeSubjectUpdateIfNecessary( )
      return self._thread
