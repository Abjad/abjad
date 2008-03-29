from abjad.containers.duration import _ContainerDurationInterface
from abjad.core.interface import _Interface
from abjad.duration.rational import Rational
from math import log

class _MeasureDurationInterface(_ContainerDurationInterface):

   ### REPR ###

   def __repr__(self):
      return 'MeasureDurationInterface(%s)' % self.contents

   ### DERIVED PROPERTIES ###

   @property
   def contents(self):
      unscaled_contents = _ContainerDurationInterface.contents.fget(self)
      if self.nonbinary:
         return unscaled_contents * self.multiplier
      else:
         return unscaled_contents

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
      if self._client.meter:
         d = self._client.meter.denominator
         return Rational(2 ** int(log(d, 2)), d)
      else:
         return Rational(1, 1)
