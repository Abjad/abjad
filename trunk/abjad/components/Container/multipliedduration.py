from abjad.components.Container.duration import _ContainerDurationInterface
from abjad.core import Rational


class _MultipliedContainerDurationInterface(_ContainerDurationInterface):

   def __init__(self, _client):
      _ContainerDurationInterface.__init__(self, _client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplier(self):
      return Rational(1)

   @property
   def preprolated(self):
      return self.multiplier * self.contents
