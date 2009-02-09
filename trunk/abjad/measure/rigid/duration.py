from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.measure.duration import _MeasureDurationInterface
from abjad.rational.rational import Rational


class _RigidMeasureDurationInterface(_MeasureDurationInterface):

   ### PUBLIC ATTRIBUTES ###

   @property
   def preprolated(self):
      return self._client.meter.effective.multiplier * self.contents
