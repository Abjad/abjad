from abjad.components.Container._MultipliedContainerDurationInterface import \
   _MultipliedContainerDurationInterface
from abjad.tools import marktools


class _MeasureDurationInterface(_MultipliedContainerDurationInterface):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      forced_meter = self._client._explicit_meter
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplier(self):
      return marktools.get_effective_time_signature(self._client).multiplier

   @property
   def is_nonbinary(self):
      return marktools.get_effective_time_signature(self._client).is_nonbinary
