from abjad.core import _Abjad
from abjad.Rational import Rational



class _SpannerDurationInterface(_Abjad):

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
      duration = Rational(0)
      for leaf in self._client.leaves:
         duration += leaf.duration.seconds
      return duration

   ## TODO: Deprecate _SpannerDurationInterface.written in favor of _SpannerDurationInterface.preprolated; this will handle LilyPond multipliers ##

   @property
   def written(self):
      '''Sum of written duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.written for component in client])
