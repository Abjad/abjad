from abjad.container.multipliedduration import _MultipliedContainerDurationInterface
from abjad.helpers.is_power_of_two import _is_power_of_two


class _TupletDurationInterface(_MultipliedContainerDurationInterface):

   def __init__(self, _client):
      _MultipliedContainerDurationInterface.__init__(self, _client)

   ### PRVIATE ATTRIBUTES ###

   @property
   def _binary(self):
      if self.multiplier:
         return _is_power_of_two(self.multiplier._n)
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
