from abjad.tools.componenttools._Component._ComponentDurationInterface import _ComponentDurationInterface
from abjad.tools import durtools


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
      if client.is_parallel: 
         return max(
            [durtools.Duration(0)] + [x.duration.preprolated for x in client])
      else:
         duration = durtools.Duration(0)
         for x in client:
            duration += x.duration.preprolated
         return duration

   @apply
   def preprolated( ):
      def fget(self):
         return self.contents
      return  property(**locals( ))

#   @property
#   def seconds(self):
#      client = self._client
#      if client.is_parallel:
#         return max([durtools.Duration(0)] + [x.duration_in_seconds for x in client])
#      else:
#         duration = durtools.Duration(0)
#         for leaf in client.leaves:
#            duration += leaf.duration_in_seconds
#         return duration
