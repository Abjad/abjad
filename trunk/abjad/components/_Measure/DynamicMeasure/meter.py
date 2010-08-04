from abjad.components._Measure.Meter import Meter
from abjad.exceptions import MeterAssignmentError
from abjad.interfaces import MeterInterface
from abjad.tools import durtools


class _DynamicMeasureMeterInterface(MeterInterface):
   '''Handle LilyPond TimeSignature grob for DynamicMeasure.
   Publish information about effective and forced meter.
   '''
   
   def __init__(self, _client, _updateInterface):
      '''Initialize parent class.'''
      MeterInterface.__init__(self, _client, _updateInterface)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _self_can_contribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      return not self.suppress

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      '''Return reference to meter effectively governing client.'''
      #client = self.client
      client = self._client
      if client.denominator:
         return Meter(
            durtools.rational_to_duration_pair_with_specified_integer_denominator(client.duration.contents, client.denominator))
      else:
         return Meter(client.duration.contents)

   @apply
   def forced( ):
      '''Read / write attribute to set meter explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         raise MeterAssignmentError
      return property(**locals( ))
