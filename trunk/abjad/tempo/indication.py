from abjad.core.abjadcore import _Abjad
from abjad.helpers.is_assignable import is_assignable
from abjad.note.note import Note
from abjad.rational.rational import Rational


class TempoIndication(_Abjad):

   def __init__(self, duration, mark):
      self.duration = duration
      self.mark = mark

   ## PUBLIC ATTRIBUTES ##

   @property
   def dotted(self):
      return Note(0, self.duration).duration._dotted

   @apply
   def duration( ):
      def fget(self):
         return self._duration
      def fset(self, arg):
         assert is_assignable(arg)
         self._duration = arg
      return property(**locals( ))

   @property
   def format(self):
      return r'\tempo %s=%s' % (self.dotted, self.mark)

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert isinstance(arg, (int, float))
         assert 0 < arg
         self._mark = arg
      return property(**locals( ))
