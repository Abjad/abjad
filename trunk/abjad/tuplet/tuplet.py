from .. containers.container import Container
from duration import _TupletDurationInterface
from formatter import TupletFormatter
from ratio import Ratio

class _Tuplet(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.brackets = 'curly'
      self._duration = _TupletDurationInterface(self)
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

   ### TODO - replace either with managed attribute OR
   ###        even better, a TupletNumber grob for
   ###        LilyPond \override TupletNumber #'fraction = True
   ###        type of dynamic overrides.

   @property
   def ratio(self):
      if self.duration.multiplier:
         return Ratio(*(~self.duration.multiplier).pair)
      else:
         return None
