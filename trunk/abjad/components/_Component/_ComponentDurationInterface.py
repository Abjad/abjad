from abjad.interfaces._Interface import _Interface
from abjad.tools import listtools
from fractions import Fraction


class _ComponentDurationInterface(_Interface):

   __slots__ = ( )

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _prolations(self):
      result = [ ]
      parent = self._client._parentage.parent
      while parent is not None:
         result.append(getattr(parent.duration, 'multiplier', Fraction(1)))
         parent = parent._parentage.parent
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def preprolated(self):
      raise NotImplementedError('_ComponentDurationInterface.preprolated not implemented.')

   @property
   def prolated(self):
      return self.prolation * self.preprolated

   @property
   def prolation(self):
      products = listtools.cumulative_products(
         [Fraction(1)] + self._prolations)
      return products[-1]
