from abjad.tools.containertools.Container._MultipliedContainerDurationInterface import _MultipliedContainerDurationInterface
from abjad.tools import contexttools


class _MeasureDurationInterface(_MultipliedContainerDurationInterface):

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      #forced_meter = self._client._explicit_meter
      if contexttools.is_component_with_time_signature_attached(self._client):
         forced_meter = contexttools.get_time_signature_mark_attached_to_component(self._client)
      else:
         forced_meter = None
      if forced_meter:
         return forced_meter.duration
      else:
         return self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def is_binary(self):
      return not self.is_nonbinary

   @property
   def is_nonbinary(self):
      return contexttools.get_effective_time_signature(self._client).is_nonbinary

   @property
   def is_overfull(self):
      '''.. versionadded:: 1.1.1

      True when prolated duration is greater than 
      effective meter duration.
      '''
      return contexttools.get_effective_time_signature(self._client).duration < self.prolated

   @property
   def is_underfull(self):
      '''.. versionadded:: 1.1.1

      True when prolated duration is less than 
      effective meter duration.
      '''
      return self.prolated < contexttools.get_effective_time_signature(self._client).duration

   @property
   def multiplier(self):
      return contexttools.get_effective_time_signature(self._client).multiplier

   @property
   def preprolated(self):
      '''Measure contents duration times effective meter multiplier.'''
      return contexttools.get_effective_time_signature(self._client).multiplier * self.contents
