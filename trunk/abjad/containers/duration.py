from .. core.duration import _DurationInterface
from .. core.interface import _Interface
from .. duration.rational import Rational
from .. helpers.hasname import hasname

class _ContainerDurationInterface(_DurationInterface):

   def __init__(self, _client):
      _DurationInterface.__init__(self, _client)

   ### REPR ###

   def __repr__(self):
      return 'ContainerDurationInterface(%s)' % self.contents

   ### READ-ONLY ATTRIBUTES ###

   @property
   def _duration(self):
      return self.contents

   @property
   def contents(self):
      duration = Rational(0)
      for x in self._client:
         duration += x.duration
      return duration
