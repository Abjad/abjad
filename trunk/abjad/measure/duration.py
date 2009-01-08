#from abjad.container.duration import _ContainerDurationInterface
from abjad.container.multipliedduration import _MultipliedContainerDurationInterface
#from abjad.core.interface import _Interface
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.rational.rational import Rational
#from math import log


#class _MeasureDurationInterface(_ContainerDurationInterface):
class _MeasureDurationInterface(_MultipliedContainerDurationInterface):

   ### PRIVATE ATTRIBUTES ###

   @property
   def _duration(self):
      #if self._client.meter:
      #   return self._client.meter.duration
      forced_meter = self._client.meter.forced
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents

   ### PUBLIC ATTRIBUTES ###

   @property
   def compression(self):
      '''Exists to handle the one exceptional case
         where a nonbinary measure has a multiplier == 1.'''
      if self.nonbinary and self.multiplier == Rational(1, 1):
         #return _denominator_to_multiplier(self._client.meter.denominator)
         return _denominator_to_multiplier(
            self._client.meter.forced.denominator)
      else:
         return self.multiplier

   ### TODO - change references from here down for
   ###        self._client.meter to self._client.meter.forced (?)

   @property
   def multiplier(self):
      #if self._client.meter and self.contents != Rational(0):
      #   return self._client.meter.duration / self.contents
      forced_meter = self._client.meter.forced
      if forced_meter and self.contents != Rational(0):
         return forced_meter.duration / self.contents
      else:
         return Rational(1, 1)

   @property
   def nonbinary(self):
      forced_meter = self._client.meter.forced
      #if self._client.meter is not None:
      #   return bool(self._client.meter.denominator & 
      #      (self._client.meter.denominator - 1))
      if forced_meter:
         return bool(forced_meter.denominator & (forced_meter.denominator - 1))
      else:
         return False

   @property
   def preprolated(self):
      forced_meter = self._client.meter.forced
      #if self._client.meter is not None:
      #   return self._client.meter.duration
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents
