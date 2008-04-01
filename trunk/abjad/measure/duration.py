from abjad.containers.duration import _ContainerDurationInterface
from abjad.core.interface import _Interface
from abjad.duration.rational import Rational
from math import log

class _MeasureDurationInterface(_ContainerDurationInterface):

   ### REPR ###

   def __repr__(self):
      return 'MeasureDurationInterface(%s)' % self._duration

   ### DERIVED PROPERTIES ###

   @property
   def _duration(self):
      if self._client.meter:
         return self._client.meter.duration
      else:
         return self.contents

   ### DERIVED PROPERTIES ###

   @property
   def nonbinary(self):
      if self._client.meter is not None:
         return bool(self._client.meter.denominator & 
            (self._client.meter.denominator - 1))
      else:
         return False

   @property
   def multiplier(self):
      if self._client.meter and self.contents != Rational(0):
         return self._client.meter.duration / self.contents
      else:
         return Rational(1, 1)
