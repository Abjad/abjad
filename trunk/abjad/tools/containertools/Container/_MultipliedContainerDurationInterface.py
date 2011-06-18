from abjad.tools.containertools.Container._ContainerDurationInterface import _ContainerDurationInterface
from abjad.tools import durtools


class _MultipliedContainerDurationInterface(_ContainerDurationInterface):

   def __init__(self, _client):
      _ContainerDurationInterface.__init__(self, _client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplier(self):
      return Duration(1)

   @property
   def preprolated(self):
      return self.multiplier * self.contents
