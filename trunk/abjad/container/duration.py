from abjad.core.duration import _DurationInterface
from abjad.rational.rational import Rational


class _ContainerDurationInterface(_DurationInterface):

   def __init__(self, _client):
      _DurationInterface.__init__(self, _client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      return self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def contents(self):
      client = self._client
      #if self._client.brackets == 'double-angle':
      if client.parallel: 
         return max(
            [Rational(0)] + [x.duration.preprolated for x in client])
      else:
         duration = Rational(0)
         for x in self._client:
            duration += x.duration.preprolated
         return duration

   @apply
   def preprolated( ):
      def fget(self):
         return self.contents
      return  property(**locals( ))
