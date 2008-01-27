#from .. duration.duration import Duration
from fmduration import _FMTupletDurationInterface
from .. duration.rational import Rational
from tuplet import _Tuplet

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

#   @apply
#   def multiplier( ):
#      def fget(self):
#         return self._multiplier
#      def fset(self, *args):
#         if isinstance(args[0], (int, long)):
#            multiplier = Rational(args[0])
#         elif isinstance(args[0], tuple):
#            multiplier = Rational(*args[0])
#         elif isinstance(args[0], Rational):
#            multiplier = Rational(*args[0].pair)
#         else:
#            raise ValueError('Can not set tuplet multiplier from %s.' % 
#               str(args))
#         if multiplier > Rational(0):
#            self._multiplier = multiplier
#         else:
#            raise ValueError('Tuplet multiplier %s must be positive.' %
#               multiplier)
#      return property(**locals( ))

   @property
   def duration(self):
      return self._duration
      #if len(self) > 0:
      #   result = self.multiplier * self.duration.composite
         #return Rational(*result.pair)
      #else:
      #   return Rational(0)

#   @property
#   def duratum(self):
#      if self.duration:
#         result = self._prolation * self.duration
#         return Duration(*result.pair)
#      else:
#         return None
