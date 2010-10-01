from abjad.components._Component._ComponentDurationInterface import _ComponentDurationInterface
from fractions import Fraction


class _ContainerDurationInterface(_ComponentDurationInterface):

   def __init__(self, _client):
      _ComponentDurationInterface.__init__(self, _client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _duration(self):
      return self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def contents(self):
      client = self._client
      if client.parallel: 
         return max(
            [Fraction(0)] + [x.duration.preprolated for x in client])
      else:
         duration = Fraction(0)
         for x in client:
            duration += x.duration.preprolated
         return duration

   @apply
   def preprolated( ):
      def fget(self):
         return self.contents
      return  property(**locals( ))

   @property
   def seconds(self):
      client = self._client
      if client.parallel:
         return max(
            [Fraction(0)] + [x.duration.seconds for x in client])
      else:
         duration = Fraction(0)
         for leaf in client.leaves:
            duration += leaf.duration.seconds
         return duration

