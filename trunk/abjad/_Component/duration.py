from abjad.interfaces._Interface import _Interface
from abjad.tools import listtools
from abjad.Rational import Rational


class _ComponentDurationInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _prolations(self):
      result = [ ]
      parent = self._client.parentage.parent
      while parent is not None:
         result.append(getattr(parent.duration, 'multiplier', Rational(1)))
         parent = parent.parentage.parent
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def preprolated(self):
      raise NotImplemented

   @property
   def prolated(self):
      return self.prolation * self.preprolated

   @property
   def prolation(self):
      products = listtools.cumulative_products(
         [Rational(1)] + self._prolations)
      return products[-1]
