from .. containers.duration import _ContainerDurationInterface
from .. core.interface import _Interface
from .. duration.rational import Rational
from .. helpers.hasname import hasname

class _TupletDurationInterface(_ContainerDurationInterface):

   def __init__(self, _client):
      _ContainerDurationInterface.__init__(self, _client)

   ### REPR ###

   def __repr__(self):
      return 'TupletDurationInterface( )'

   ### PREDICATES ###

   @property
   def _binary(self):
      if self.multiplier:
         return not self.multiplier._n & (self.multiplier._n - 1)
      else:
         return True

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
