from abjad.core.interface import _Interface
from abjad.tools import mathtools
from abjad.rational.rational import Rational


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
      products = mathtools.products([Rational(1)] + self._prolations)
      return products[-1]
