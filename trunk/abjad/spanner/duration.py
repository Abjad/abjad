from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational



class _SpannerDurationInterface(_Abjad):

   def __init__(self, _client):
      self._client = _client

   ## PUBLIC ATTRIBUTES ##

   @property
   def clock(self):
      '''Sum of clock duration of all leaves in spanner.'''
      duration = Rational(0)
      for leaf in self._client.leaves:
         duration += leaf.duration.clock
      return duration

   @property
   def prolated(self):
      '''Sum of prolated duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.prolated for component in client])

   @property
   def written(self):
      '''Sum of written duration of all components in spanner.'''
      client = self._client
      return sum([component.duration.written for component in client])
