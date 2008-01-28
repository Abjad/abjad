from ... duration.rational import Rational
from duration import _FDTupletDurationInterface
from .. tuplet import _Tuplet

class FixedDurationTuplet(_Tuplet):

   def __init__(self, duration, music):
      _Tuplet.__init__(self, music)
      self._duration = _FDTupletDurationInterface(self, duration)
      self._signifier = '@'
      #self.duration.fixed = duration
      #self.duration._n = duration[0]
      #self.duration._d = duration[1]

   ### REPR ###
 
   def __repr__(self):
      return 'FixedDurationTuplet(%s, [%s])' % (
         #self.duration.fixed, self._summary)
         self.duration, self._summary)

   def __str__(self):
      if len(self) > 0:
         return '{%s %s %s %s}' % (
            self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (
            #self._signifier, self.duration.fixed, self._signifier)
            self._signifier, self.duration, self._signifier)

   ### MANAGED ATTRIBUTES ###

   @apply
   def duration( ):
      def fget(self):
         return self._duration
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = Rational(expr)
         elif isinstance(expr, tuple):
            rational = Rational(*expr)
         elif isinstance(expr, Rational):
            rational = Rational(*expr.pair)
         else:
            raise ValueError('Can not set tuplet rational from %s.' % 
               str(expr))
         if rational > 0:
            self.duration._duration = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))
