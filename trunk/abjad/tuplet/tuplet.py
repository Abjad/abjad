from .. containers.container import Container
from .. duration.duration import Duration
from ratio import Ratio
from formatter import TupletFormatter

class _Tuplet(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.brackets = 'curly'
      self.formatter = TupletFormatter(self) 

   ### REPR ###

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   def __repr__(self):
      if len(self) > 0:
         return '_Tuplet(%s)' % self._summary
      else:
         return '_Tuplet( )'

   ### PROPERTIES ###

   @property
   def ratio(self):
      if self.multiplier:
         return Ratio(*(~self.multiplier).pair)
      else:
         return None

   @property
   def _musicDuration(self):
      result = [ ]
      for x in self._music:
         if x.kind('Leaf'):
            if x.duration and x.multiplier:
               result.append(x.duration * x.multiplier)
            elif x.duration:
               result.append(x.duration)
            else:
               pass
         elif x.kind('_Tuplet'):
            result.append(x.duration)
      return sum(result, Duration(0))

   @property
   def duratum(self):
      result = self._parentage._prolation * self.duration
      return Duration(*result.pair)

   ### PREDICATES ###

   def isBinary(self):
      if self.multiplier:
         return not self.multiplier._n & (self.multiplier._n - 1)
      else:
         return True

   def isAugmentation(self):
      if self.multiplier:
         return self.multiplier > 1
      else:
         return False

   def isDiminution(self):
      if self.multiplier:
         return self.multiplier < 1
      else:
         return False
