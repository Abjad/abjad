from abjad.components.Container._MultipliedContainerDurationInterface import \
   _MultipliedContainerDurationInterface


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
