from abjad.Container.duration import _ContainerDurationInterface
from abjad.Rational import Rational


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
