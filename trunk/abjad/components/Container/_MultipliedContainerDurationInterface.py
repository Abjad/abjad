from abjad.components.Container._ContainerDurationInterface import _ContainerDurationInterface
from abjad.core import Fraction


class _MultipliedContainerDurationInterface(_ContainerDurationInterface):

   def __init__(self, _client):
      _ContainerDurationInterface.__init__(self, _client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplier(self):
      return Fraction(1)

   @property
   def preprolated(self):
      return self.multiplier * self.contents
