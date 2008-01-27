from .. core.duration import _DurationInterface
from .. core.interface import _Interface
from .. duration.rational import Rational
from .. helpers.hasname import hasname

class _ContainerDurationInterface(_DurationInterface):

   def __init__(self, _client):
      _DurationInterface.__init__(self, _client)

   ### REPR ###

   def __repr__(self):
      return 'ContainerDurationInterface( )'

   ### READ-ONLY ATTRIBUTES ###

   @property
   def composite(self):
      duration = Rational(0)
      for x in self._client:
         if hasname(x, 'Leaf'):
            duration += x.duration._multiplied
         elif hasname(x, '_Tuplet'):
            duration += x.duration.resultant
         else:
            duration += x.duration.composite
      return duration

   @property
   def absolute(self):
      return self.prolation * self.composite
