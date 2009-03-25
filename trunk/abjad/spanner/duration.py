from abjad.core.abjadcore import _Abjad


class _SpannerDurationInterface(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PUBLIC ATTRIBUTES ##

   @property
   def prolated(self):
      client = self._client
      return sum([component.duration.prolated for component in client])

   @property
   def written(self):
      client = self._client
      return sum([component.duration.written for component in client])
