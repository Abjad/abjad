from abjad.components.Measure._MeasureDurationInterface import _MeasureDurationInterface
from abjad.tools import marktools


class _RigidMeasureDurationInterface(_MeasureDurationInterface):

#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def is_overfull(self):
#      '''.. versionadded:: 1.1.1
#
#      True when prolated duration is greater than 
#      effective meter duration.
#      '''
#
#      return marktools.get_effective_time_signature(self._client).duration < self.prolated
#      
#
#   @property
#   def is_underfull(self):
#      '''.. versionadded:: 1.1.1
#
#      True when prolated duration is less than 
#      effective meter duration.
#      '''
#
#      return self.prolated < marktools.get_effective_time_signature(self._client).duration
#
#   @property
#   def preprolated(self):
#      '''Measure contents duration times effective meter multiplier.'''
#      return marktools.get_effective_time_signature(self._client).multiplier * self.contents

   pass
