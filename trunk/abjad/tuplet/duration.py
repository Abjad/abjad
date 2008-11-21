#from abjad.containers.duration import _ContainerDurationInterface
from abjad.containers.multipliedduration import _MultipliedContainerDurationInterface
#from abjad.core.interface import _Interface
#from abjad.helpers.hasname import hasname
#from abjad.rational.rational import Rational


#class _TupletDurationInterface(_ContainerDurationInterface):
class _TupletDurationInterface(_MultipliedContainerDurationInterface):

   def __init__(self, _client):
      #_ContainerDurationInterface.__init__(self, _client)
      _MultipliedContainerDurationInterface.__init__(self, _client)

#   ### OVERLOADS ###
#
#   def __repr__(self):
#      return 'TupletDurationInterface( )'

   ### PRVIATE ATTRIBUTES ###

   @property
   def _binary(self):
      if self.multiplier:
         return not self.multiplier._n & (self.multiplier._n - 1)
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
