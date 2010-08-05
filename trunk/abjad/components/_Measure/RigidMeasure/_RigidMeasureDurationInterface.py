from abjad.components._Measure._MeasureDurationInterface import _MeasureDurationInterface


class _RigidMeasureDurationInterface(_MeasureDurationInterface):

   ## PUBLIC ATTRIBUTES ##

   @property
   def is_overfull(self):
      '''.. versionadded:: 1.1.1

      True when prolated duration is greater than 
      effective meter duration.
      '''

      return self.prolated > self._client.meter.effective.duration

   @property
   def is_underfull(self):
      '''.. versionadded:: 1.1.1

      True when prolated duration is less than 
      effective meter duration.
      '''

      return self.prolated < self._client.meter.effective.duration

   @property
   def preprolated(self):
      '''Measure contents duration times effective meter multiplier.'''
      return self._client.meter.effective.multiplier * self.contents
