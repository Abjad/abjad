from duration import _FMTupletDurationInterface
from ... duration.rational import Rational
from .. tuplet import _Tuplet

class FixedMultiplierTuplet(_Tuplet):

   def __init__(self, multiplier, music = [ ]):
      _Tuplet.__init__(self, music)
      self._duration = _FMTupletDurationInterface(self, self)
      self._signifier = '*'
      self.duration.multiplier = multiplier

   ### REPR ###

   def __repr__(self):
      return 'FixedMultiplierTuplet(%s, [%s])' % ( 
         self.duration.multiplier, self._summary)

   def __str__(self):
      if len(self) > 0:
         return '{%s %s %s %s}' % (
            self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (
            self._signifier, self.duration.multiplier, self._signifier)

   ### PROPERTIES ###

   @property
   def duration(self):
      return self._duration
      #if len(self) > 0:
      #   result = self.multiplier * self.duration.composite
         #return Rational(*result.pair)
      #else:
      #   return Rational(0)
