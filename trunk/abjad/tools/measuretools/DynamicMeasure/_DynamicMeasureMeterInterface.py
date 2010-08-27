from abjad.tools.metertools import Meter
from abjad.exceptions import MeterAssignmentError
from abjad.interfaces import MeterInterface
from abjad.tools import durtools
from abjad.tools import marktools


class _DynamicMeasureMeterInterface(MeterInterface):
   '''Handle LilyPond TimeSignature grob for DynamicMeasure.
   Publish information about effective and forced meter.
   '''

   pass
   
#   def __init__(self, _client, _update_interface):
#      '''Initialize parent class.'''
#      MeterInterface.__init__(self, _client, _update_interface)
#
#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _self_can_contribute(self):
#      r'''True when self is able to contribute LilyPond \time.'''
#      return not self.suppress
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def effective(self):
#      '''Return reference to meter effectively governing client.'''
#      client = self._client
#      if client.denominator:
#         meter = Meter(
#            durtools.rational_to_duration_pair_with_specified_integer_denominator(
#               client.duration.contents, client.denominator))
#      else:
#         meter = Meter(client.duration.contents)
#      #return meter
#      meter = marktools.TimeSignatureMark(meter.numerator, meter.denominator)
#      client._attach_explicit_meter(meter)
#      return meter
#
#   @apply
#   def forced( ):
#      '''Read / write attribute to set meter explicitly.'''
#      def fget(self):
#         return self._forced
#      def fset(self, arg):
#         raise MeterAssignmentError
#      return property(**locals( ))
