from abjad.containers.duration import _ContainerDurationInterface
from .. core.interface import _Interface
from .. duration.rational import Rational
from .. helpers.hasname import hasname

class _MeasureDurationInterface(_ContainerDurationInterface):

   ### REPR ###

   def __repr__(self):
      return 'MeasureDurationInterface(%s)' % self.contents

   ### DERIVED PROPERTIES ###

   @property
   def contents(self):
      unscaled_contents = _ContainerDurationInterface.contents.fget(self)
      if self._client.nonbinary:
         return unscaled_contents * Rational(*self._client._multiplier)
      else:
         return unscaled_contents
