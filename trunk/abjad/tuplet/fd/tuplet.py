from abjad.duration.rational import Rational
from abjad.tuplet.fd.duration import _FDTupletDurationInterface
from abjad.tuplet.tuplet import _Tuplet

class FixedDurationTuplet(_Tuplet):

   def __init__(self, duration, music):
      _Tuplet.__init__(self, music)
      self._duration = _FDTupletDurationInterface(self, duration)
      self._signifier = '@'

   ### REPR ###
 
   def __repr__(self):
      return 'FixedDurationTuplet(%s, [%s])' % (
         self.duration, self._summary)

   def __str__(self):
      if len(self) > 0:
         return '{%s %s %s %s}' % (
            self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (
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


   ### BOUND METHODS ###

   def trim(self, start, stop = 'unused'):
      assert not (start == 0 and (stop is None or stop >= len(self)))
      old_multiplier = self.duration.multiplier
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start : stop])
      self.duration = old_multiplier * self.duration.contents
