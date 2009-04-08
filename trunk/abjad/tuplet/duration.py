from abjad.container.multipliedduration import \
   _MultipliedContainerDurationInterface
from abjad.tools import mathtools


class _TupletDurationInterface(_MultipliedContainerDurationInterface):

   def __init__(self, _client):
      _MultipliedContainerDurationInterface.__init__(self, _client)

   ### PRVIATE ATTRIBUTES ###

   @property
   def _binary(self):
      if self.multiplier:
         return mathtools.is_power_of_two(self.multiplier._n)
      else:
         return True

   ### PUBLIC ATTRIBUTES ###

   @property
   def augmentation(self):
      if self.multiplier:
         return self.multiplier > 1
      else:
         return False

   @property
   def diminution(self):
      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @property
   def preprolated(self):
      return self.multiplied
