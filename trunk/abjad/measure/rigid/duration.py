from abjad.measure.duration import _MeasureDurationInterface


class _RigidMeasureDurationInterface(_MeasureDurationInterface):

   ### PUBLIC ATTRIBUTES ###

   @property
   def preprolated(self):
      return self._client.meter.effective.multiplier * self.contents
