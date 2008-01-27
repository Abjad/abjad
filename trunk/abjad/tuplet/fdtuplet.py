from .. duration.rational import Rational
from fdduration import _FDTupletDurationInterface
from tuplet import _Tuplet

class FixedDurationTuplet(_Tuplet):

   def __init__(self, duration, music):
      _Tuplet.__init__(self, music)
      self._duration = _FDTupletDurationInterface(self, self)
      self._signifier = '@'
      self.duration.fixed = duration

   ### REPR ###
 
   def __repr__(self):
      return 'FixedDurationTuplet(%s, [%s])' % (
         self.duration.fixed, self._summary)

   def __str__(self):
      if len(self) > 0:
         return '{%s %s %s %s}' % (
            self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (
            self._signifier, self.duration.fixed, self._signifier)

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
            self.duration.fixed = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))
