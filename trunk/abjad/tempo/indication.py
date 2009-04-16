from abjad.core.abjadcore import _Abjad
from abjad.tools import durtools
from abjad.rational.rational import Rational


class TempoIndication(_Abjad):
   '''Tempo indication token.
      Assign to _TempoInterface.indication.'''

   def __init__(self, duration, mark):
      '''Set duration and mark.'''
      self.duration = duration
      self.mark = mark

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, TempoIndication):
         if self.duration == expr.duration:
            if self.mark == expr.mark:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dotted(self):
      '''Dotted numeral representation of duration.'''
      from abjad.note.note import Note
      return Note(0, self.duration).duration._dotted

   ## PUBLIC ATTRIBUTES ##

   @apply
   def duration( ):
      '''Duration of tempo indication.'''
      def fget(self):
         return self._duration
      def fset(self, arg):
         assert durtools.is_assignable(arg)
         self._duration = arg
      return property(**locals( ))

   @property
   def format(self):
      '''Tempo indication as string.'''
      return r'\tempo %s=%s' % (self._dotted, self.mark)

   @apply
   def mark( ):
      '''Metronome mark value of tempo indication.'''
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert isinstance(arg, (int, float))
         assert 0 < arg
         self._mark = arg
      return property(**locals( ))
