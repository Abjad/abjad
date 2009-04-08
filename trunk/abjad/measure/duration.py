from abjad.container.multipliedduration import _MultipliedContainerDurationInterface
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.tools import mathtools
from abjad.rational.rational import Rational


class _MeasureDurationInterface(_MultipliedContainerDurationInterface):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      forced_meter = self._client.meter.forced
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplier(self):
      return self._client.meter.effective.multiplier

   @property
   def nonbinary(self):
      return self._client.meter.effective.nonbinary
