from abjad.core import _StrictComparator
from abjad.tools import durtools


class _SpannerDurationInterface(_StrictComparator):

   def __init__(self, _client):
      self._client = _client

   ## PUBLIC ATTRIBUTES ##

   @property
   def preprolated(self):
      '''Sum of preprolated duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.preprolated for component in client])

   @property
   def prolated(self):
      '''Sum of prolated duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.prolated for component in client])

   @property
   def seconds(self):
      '''Sum of duration of all leaves in spanner, in seconds.'''
      duration = durtools.Duration(0)
      for leaf in self._client.leaves:
         duration += leaf.duration.seconds
      return duration

   ## TODO: Deprecate _SpannerDurationInterface.written in favor of _SpannerDurationInterface.preprolated; this will handle LilyPond multipliers ##

   @property
   def written(self):
      '''Sum of written duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.written for component in client])
