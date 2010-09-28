from abjad.core import _StrictComparator
from abjad.core import Fraction


class _SpannerOffsetInterface(_StrictComparator):

   def __init__(self, client):
      self._client = client

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def start(self):
      client = self._client
      if len(client):
         return client[0].offset.start
      else:
         return Fraction(0)

   @property
   def stop(self):
      client = self._client
      if len(client):
         last = client[-1]
         return last.offset.stop
      else:
         return Fraction(0)
