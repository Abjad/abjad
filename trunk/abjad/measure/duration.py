from abjad.containers.duration import _ContainerDurationInterface
from abjad.core.interface import _Interface
from abjad.duration.rational import Rational
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from math import log


class _MeasureDurationInterface(_ContainerDurationInterface):

#   ### OVERLOADS ###
#
#   def __repr__(self):
#      return 'MeasureDurationInterface(%s)' % self._duration

   ### PRIVATE ATTRIBUTES ###

   @property
   def _duration(self):
      if self._client.meter:
         return self._client.meter.duration
      else:
         return self.contents

   ### PUBLIC ATTRIBUTES ###

   @property
   def compression(self):
      '''Exists to handle the one exceptional case
         where a nonbinary measure has a multiplier == 1.'''
      if self.nonbinary and self.multiplier == Rational(1, 1):
         return _denominator_to_multiplier(self._client.meter.denominator)
      else:
         return self.multiplier

   @property
   def multiplier(self):
      if self._client.meter and self.contents != Rational(0):
         return self._client.meter.duration / self.contents
      else:
         return Rational(1, 1)

   @property
   def nonbinary(self):
      if self._client.meter is not None:
         return bool(self._client.meter.denominator & 
            (self._client.meter.denominator - 1))
      else:
         return False

   @property
   def preprolated(self):
      if self._client.meter is not None:
         return self._client.meter.duration
      else:
         return self.contents
