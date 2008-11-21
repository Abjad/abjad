from abjad.core.interface import _Interface
#from abjad.helpers.hasname import hasname
#from abjad.helpers.rationalize import _rationalize
from abjad.rational.rational import Rational
from operator import mul


class _DurationInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _prolations(self):
      result = [ ]
      parent = self._client._parent
      while parent is not None:
         result.append(parent.duration.multiplier)
         parent = parent._parent
      return result

   ### PUBLIC ATTRIBUTES ###

   @property
   def preprolated(self):
      raise NotImplemented

   @property
   def prolated(self):
      return self.prolation * self.preprolated

   @property
   def prolation(self):
      return reduce(mul, self._prolations, Rational(1))
