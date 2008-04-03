#from .. core.duration import _DurationInterface
#from .. core.interface import _Interface
#from .. duration.rational import Rational

from abjad.core.duration import _DurationInterface
from abjad.core.interface import _Interface
from abjad.duration.rational import Rational

class _ContainerDurationInterface(_DurationInterface):

   def __init__(self, _client):
      _DurationInterface.__init__(self, _client)

   ### REPR ###

   def __repr__(self):
      return 'ContainerDurationInterface(%s)' % self.contents

   ### DERIVED ATTRIBUTES ###

   @property
   def _duration(self):
      return self.contents

   @property
   def contents(self):
      if self._client.brackets == 'double-angle':
         return max([Rational(0)] + [x.duration for x in self._client])
      else:
         duration = Rational(0)
         for x in self._client:
            duration += x.duration
         return duration

   @property
   def multiplier(self):
      return Rational(1)
