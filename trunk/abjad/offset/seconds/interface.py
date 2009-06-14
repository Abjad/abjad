from abjad.core.observer import _Observer
from abjad.exceptions.exceptions import UndefinedTempoError
from abjad.rational import Rational


class _OffsetSecondsInterface(_Observer):
   '''Serve rational-valued start and stop values in seconds.'''

   def __init__(self, _client, _updateInterface):
      '''Bind to _OffsetInterface as client.
         Register self as observer.
         Init start and stop to zero.'''
      _Observer.__init__(self, _client, _updateInterface)
      self._start = Rational(0)
      self._stop = Rational(0)

   ## PRIVATE METHODS ##

   def _update(self):
      '''Update offset values of any one node in score.'''
      self._updateStart( )

   def _updateStart(self):
      '''Update prolated start from score start.
         Updating prolated stop here induces infinite recursion.'''
      prev = self._client._client._navigator._prev
      if prev:
         try:
            self._start = prev.offset.seconds.stop
         except UndefinedTempoError:
            self._start = Rational(0)
      else:
         self._start = Rational(0)

   ## PUBLIC ATTRIBUTES ##

   @property
   def start(self):
      '''Rational-valued rhythmic start point from beginning of score.'''
      self._makeSubjectUpdateIfNecessary( )
      if self._client._client.tempo.effective is None:
         raise UndefinedTempoError
      return self._start

   @property
   def stop(self):
      '''Rational-valued rhythmic stop point from beginning of score.'''
      return self.start + self._client._client.duration.seconds
