from abjad.exceptions import UndefinedTempoError
#from abjad.interfaces._Interface import _Interface
from abjad.interfaces._ObserverInterface import _ObserverInterface
#from abjad.interfaces.OffsetInterface._OffsetProlatedInterface import _OffsetProlatedInterface
#from abjad.interfaces.OffsetInterface._OffsetSecondsInterface import _OffsetSecondsInterface
from abjad.core import Rational


#class OffsetInterface(_Interface):
class OffsetInterface(_ObserverInterface):
   '''Offset interface.
   '''

   def __init__(self, _client, _updateInterface):
      #_Interface.__init__(self, _client)
      _ObserverInterface.__init__(self, _client, _updateInterface)
      #self._prolated = _OffsetProlatedInterface(self, _updateInterface)
      #self._seconds = _OffsetSecondsInterface(self, _updateInterface)
      self._start = Rational(0)
      self._start_in_seconds = Rational(0)
      self._stop = Rational(0)
      self._stop_in_seconds = Rational(0)

   ## PRIVATE METHODS ##

   def _update(self):
      '''Update offset values of any one node in score.'''
      self._update_start( )

   def _update_start(self):
      '''Update prolated start time and start time in seconds.
      Updating stop at same time induces infinite recursion.
      '''
      prev = self._client._navigator._prev
      if prev:
         self._start = prev.offset.stop
         try:
            self._start_in_seconds = prev.offset.stop_in_seconds
         except UndefinedTempoError:
            self._start_in_seconds = Rational(0)
      else:
         self._start = Rational(0)
         self._start_in_seconds = Rational(0)

   ## PUBLIC ATTRIBUTES ##

#   @property
#   def prolated(self):
#      return self._prolated
#  
#   @property
#   def seconds(self):
#      return self._seconds

   @property
   def start(self):
      self._make_subject_update_if_necessary( )
      return self._start

   @property
   def stop(self):
      return self.start + self._client.duration.prolated

   @property
   def start_in_seconds(self):
      self._make_subject_update_if_necessary( )
      return self._start_in_seconds

   @property
   def stop_in_seconds(self):
      return self.start_in_seconds + self._client.duration.seconds
