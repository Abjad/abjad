from abjad.core.duration import _DurationInterface
from abjad.rational.rational import Rational


class _ContainerDurationInterface(_DurationInterface):

   def __init__(self, _client):
      _DurationInterface.__init__(self, _client)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _duration(self):
      return self.contents

   ### PUBLIC ATTRIBUTES ###

   @property
   def contents(self):
      if self._client.brackets == 'double-angle':
         # FIXME: the x.duration is now illegal
         # must be x.duration.something instead
         #return max([Rational(0)] + [x.duration for x in self._client])
         return max(
            [Rational(0)] + [x.duration.preprolated for x in self._client])
      else:
         duration = Rational(0)
         for x in self._client:
            # TODO: some sort of x.duration.preprolated
            # would elminiate the isinstance( ) here
            #duration += x.duration

            #if hasattr(x.duration, 'target'):
            #   duration += x.duration.target
            #else:
            #   duration += x.duration
            
            duration += x.duration.preprolated
         return duration

#   @property
#   def multiplier(self):
#      return Rational(1)

   @apply
   def preprolated( ):
      def fget(self):
         #return self.contents   
         #return self.multiplier * self.contents   
         return self.contents
      return  property(**locals( ))
