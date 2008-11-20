from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname
from abjad.helpers.rationalize import _rationalize
from abjad.rational.rational import Rational
from operator import mul


### TODO: sever _DurationInterface's inheritance from Rational;
###       this will be a relatively big change;
###       calculations and comparison will no longer be
###       possible on _DurationInterface and its children,
###       including _LeafDurationInterface.
###       This means that t.duration == Rational(1, 4)
###       will no longer be allowed;
###       we will have to use t.duration.written == Rational(1, 4)
###       or t.duration.prolated == Rational(1, 4) instead.
###       See other TODO, below for why this is a good idea.

#class _DurationInterface(_Interface, Rational):
class _DurationInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)
      #Rational.__init__(self, 1)

#   ### OVERLOADS ###
#
#   @_rationalize
#   def __eq__(self, arg):
#      return Rational.__eq__(self, arg) 

#   ### PRIVATE ATTRIBUTES ### 
#
#   @property
#   def _d(self):
#      return self._duration._d
#
#   @property
#   def _n(self):  
#      return self._duration._n
         
   ### PUBLIC ATTRIBUTES ###

   @property
   def prolation(self):
      #return reduce(mul, self.prolations, Rational(1))
      return reduce(mul, self._prolations, Rational(1))

   @property
   def prolated(self):
      #return self.prolation * self
      #if hasattr(self, 'target'):
      #   return self.prolation * self.target
      #else:
      #   #return self.prolation * self
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
      return self.prolation * self.preprolated

   @property
   #def prolations(self):
   def _prolations(self):
      result = [ ]
      parent = self._client._parent
      while parent is not None:
         result.append(parent.duration.multiplier)
         parent = parent._parent
      return result
