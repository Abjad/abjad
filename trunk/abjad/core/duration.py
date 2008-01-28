from .. duration.rational import Rational
from .. helpers.hasname import hasname
from interface import _Interface

class _DurationInterface(_Interface, Rational):

   def __init__(self, _client):
      _Interface.__init__(self, _client, None, [ ])
      Rational.__init__(self, 1)

   ### READ-ONLY ATTRIUTES ###

   @property
   def _n(self):  
      #return self.absolute._n 
      return self._duration._n
         
   @property
   def _d(self):
      #return self.absolute._d
      return self._duration._d

   @property
   def prolation(self):
      result = Rational(1)
      t = self._client._parent
      while t is not None:
         if hasname(t, '_Tuplet'):
            result *= t.duration.multiplier
         t = t._parent
      return result

   @property
   def prolated(self):
      return self.prolation * self
