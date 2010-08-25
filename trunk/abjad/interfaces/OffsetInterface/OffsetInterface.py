from abjad.exceptions import UndefinedTempoError
#from abjad.interfaces._Interface import _Interface
from abjad.interfaces._ObserverInterface import _ObserverInterface
from abjad.core import Rational


class OffsetInterface(_ObserverInterface):
#class OffsetInterface(_Interface):
   '''Offset interface.
   '''

   __slots__ = ('_start', '_start_in_seconds', '_stop', '_stop_in_seconds')

   def __init__(self, _client, _update_interface):
      _ObserverInterface.__init__(self, _client, _update_interface)
      #_Interface.__init__(self, _client)
      self._start = None
      self._start_in_seconds = None
      self._stop = None
      self._stop_in_seconds = None

   ## PRIVATE METHODS ##

   def _update_component(self):
      #'''Update offset values of any one node in score.'''
      #self._update_component_start_offset_values( )
      pass
      #self._update_offset_values_of_component_in_seconds( )

#   def _update_all_offset_values_of_component(self):
#      '''Specialized method designed to allow update of all offset values
#      of all score components prior to updating all remaining observer
#      interfaces of all components in a second pass through the entire score.
#      '''
#      self._update_prolated_offset_values_of_component( )
#      self._update_offset_values_of_component_in_seconds( )

   def _update_offset_values_of_component_in_seconds(self):
      try:
         cur_duration_in_seconds = self._client.duration.seconds
         prev = self._client._navigator._prev
         if prev:
            self._start_in_seconds = prev.offset.stop_in_seconds
         else:
            self._start_in_seconds = Rational(0)
         self._stop_in_seconds = self._start_in_seconds + cur_duration_in_seconds
      except UndefinedTempoError:
         pass
      
   def _update_prolated_offset_values_of_component(self):
      prev = self._client._navigator._prev
      if prev:
         self._start = prev.offset._stop
      else:
         self._start = Rational(0)
      self._stop = self._start + self._client.duration.prolated

#   def _update_component_start_offset_values(self):
#      '''Update prolated start time and start time in seconds.
#      Updating stop at same time induces infinite recursion.
#      '''
#      prev = self._client._navigator._prev
#      if prev:
#         self._start = prev.offset.stop
#         try:
#            self._start_in_seconds = prev.offset.stop_in_seconds
#         except UndefinedTempoError:
#            self._start_in_seconds = Rational(0)
#      else:
#         self._start = Rational(0)
#         self._start_in_seconds = Rational(0)

   ## PUBLIC ATTRIBUTES ##

   @property
   def start(self):
#      self._update_all_observer_interfaces_in_score_if_necessary( )
#      return self._start
      self._update_prolated_offset_values_of_all_score_components_if_necessary( )
      return self._start

   @property
   def stop(self):
#      #return self.start + self._client.duration.prolated
      self._update_prolated_offset_values_of_all_score_components_if_necessary( )
      return self._stop

   @property
   def start_in_seconds(self):
#      self._update_all_observer_interfaces_in_score_if_necessary( )
#      return self._start_in_seconds
#      return self.start_in_seconds + self._client.duration.seconds
      self._update_observer_interfaces_of_all_score_components_if_necessary( )
      if self._start_in_seconds is None:
         raise UndefinedTempoError
      return self._start_in_seconds

   @property
   def stop_in_seconds(self):
#      return self.start_in_seconds + self._client.duration.seconds
      self._update_observer_interfaces_of_all_score_components_if_necessary( )
      if self._stop_in_seconds is None:
         raise UndefinedTempoError
      return self._stop_in_seconds
