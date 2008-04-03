from abjad.duration.rational import Rational
from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname
from operator import mul

### TODO: put in helpers directory? Make a decorators folder?
### Don't need to use decorators to allow X.duration == (n, m), 
### but could be useful elsewhere?
def _rationalize(meth):
   '''Convert method argument from list or tuple to Rational.
      meth((m, n)) --> meth(Rational(m, n))
   '''
   def new(self, arg):
      if isinstance(arg, (list, tuple)):
         assert len(arg) < 3
         arg = Rational(*arg)
      return meth(self, arg)
   return new


class _DurationInterface(_Interface, Rational):

   def __init__(self, _client):
      _Interface.__init__(self, _client, None, [ ])
      Rational.__init__(self, 1)

   ### READ-ONLY ATTRIUTES ###

   @property
   def _n(self):  
      return self._duration._n
         
   @property
   def _d(self):
      return self._duration._d

   @property
   def prolations(self):
      result = [ ]
      parent = self._client._parent
      while parent is not None:
         result.append(parent.duration.multiplier)
         parent = parent._parent
      return result

   @property
   def prolation(self):
      return reduce(mul, self.prolations, Rational(1))

   @property
   def prolated(self):
      return self.prolation * self


   ### OVERRIDES ###

   @_rationalize
   def __eq__(self, arg):
      return Rational.__eq__(self, arg) 
