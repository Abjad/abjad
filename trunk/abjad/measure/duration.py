from abjad.container.multipliedduration import _MultipliedContainerDurationInterface
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.rational.rational import Rational


class _MeasureDurationInterface(_MultipliedContainerDurationInterface):

   ### PRIVATE ATTRIBUTES ###

   @property
   def _duration(self):
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
         denominator = self._client.meter.forced.denominator
         return _denominator_to_multiplier(denominator)
      else:
         return self.multiplier

   @property
   def multiplier(self):
      forced_meter = self._client.meter.forced
      if forced_meter and self.contents != Rational(0):
         return forced_meter.duration / self.contents
      else:
         return Rational(1, 1)

   @property
   def nonbinary(self):
      forced_meter = self._client.meter.forced
      if forced_meter:
         return not _is_power_of_two(forced_meter.denominator)
      else:
         return False

   @property
   def preprolated(self):
      forced_meter = self._client.meter.forced
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents
