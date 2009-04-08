from abjad.exceptions.exceptions import MeterAssignmentError
from abjad.tools import mathtools
from abjad.meter.meter import Meter
from abjad.meter.interface import _MeterInterface


class _DynamicMeasureMeterInterface(_MeterInterface):
   '''Handle LilyPond TimeSignature grob for DynamicMeasure.
      Publish information about effective and forced meter.'''
   
   def __init__(self, _client):
      '''Initialize parent class.'''
      _MeterInterface.__init__(self, _client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      return not self.suppress

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      '''Return reference to meter effectively governing client.'''
      client = self.client
      if client.denominator:
         return Meter(
            mathtools.in_terms_of(client.duration.contents, client.denominator))
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
