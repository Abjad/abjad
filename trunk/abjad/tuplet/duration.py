from abjad.container.multipliedduration import \
   _MultipliedContainerDurationInterface
from abjad.tools import mathtools


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   '''Manage tuplet duration attributes.'''

   def __init__(self, _client):
      '''Bind to client.
         Init as type of multiplied container duration interface.'''
      _MultipliedContainerDurationInterface.__init__(self, _client)

   ### PRVIATE ATTRIBUTES ###

   @property
   def _binary(self):
      '''True when multiplier numerator is power of two, otherwise False.'''
      if self.multiplier:
         return mathtools.is_power_of_two(self.multiplier._n)
      else:
         return True

   ### PUBLIC ATTRIBUTES ###

   @property
   def augmentation(self):
      '''True when multiplier is greater than one, otherwise False.'''
      if self.multiplier:
         return self.multiplier > 1
      else:
         return False

   @property
   def diminution(self):
      '''True when multiplier is less than one, otherwise False.'''
      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @property
   def preprolated(self):
      '''Duration prior to prolation.'''
      return self.multiplied
