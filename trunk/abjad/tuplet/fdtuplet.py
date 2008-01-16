from .. duration.duration import Duration
from .. duration.rational import Rational
from tuplet import _Tuplet

class FixedDurationTuplet(_Tuplet):

   def __init__(self, duration, music):
      _Tuplet.__init__(self, music)
      self.duration = duration
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
      def fset(self, *args):
         if isinstance(args[0], (int, long)):
            duration = Duration(args[0])
         elif isinstance(args[0], tuple):
            duration = Duration(*args[0])
         elif isinstance(args[0], Rational):
            duration = Duration(*args[0].pair)
         else:
            raise ValueError('Can not set tuplet duration from %s.' % 
               str(args))
         if duration > Duration(0):
            self._duration = duration
         else:
            raise ValueError('Tuplet duration %s must be positive.' %
               duration)
      return property(**locals( ))

   @property
   def multiplier(self):
      if len(self) > 0:
         result = self.duration / self._musicDuration
         return Rational(*result.pair)
      else:
         return None
