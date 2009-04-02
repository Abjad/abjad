from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational


class _SpannerOffsetInterface(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def start(self):
      client = self._client
      if len(client):
         return client[0].offset.score
      else:
         return Rational(0)

   @property
   def stop(self):
      client = self._client
      if len(client):
         last = client[-1]
         return last.offset.score + last.duration.prolated
      else:
         return Rational(0)
