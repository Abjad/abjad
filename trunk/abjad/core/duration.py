from abjad.duration.rational import Rational
from abjad.core.interface import _Interface
#from abjad.core.trivialinterface import _TrivialInterface
from abjad.helpers.hasname import hasname
from abjad.helpers.rationalize import _rationalize
from operator import mul


#class _DurationInterface(_Interface, Rational):
#class _DurationInterface(_TrivialInterface, Rational):
class _DurationInterface(_Interface, Rational):

   def __init__(self, _client):
      #_Interface.__init__(self, _client, None, [ ])
      #_TrivialInterface.__init__(self, _client)
      _Interface.__init__(self, _client)
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
      #return self.prolation * self
      # EVENTUALLY: self.prolation * self.preprolated
      if hasattr(self, 'target'):
         return self.prolation * self.target
      else:
         return self.prolation * self
   # TODO:
   # this sort of reference to 'self' as the _DurationInterface
   # itself is confusing;
   # this sort of code should clean up when we implement 
   # absolute duration explicitly as duration.absolute,
   # and when we implement multiplied duration explicitly as
   # duration.multiplied.
   # I'm still confused as to which of the different duration 
   # attributes 'self' is supposed to model here;
   # would prefer to allow *no math* against self and 
   # *only comparisons* against self.

   ### OVERRIDES ###

   @_rationalize
   def __eq__(self, arg):
      return Rational.__eq__(self, arg) 
