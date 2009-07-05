from abjad.core.abjadcore import _Abjad
from abjad.tools import durtools
from abjad.rational import Rational


class TempoIndication(_Abjad):
   r'''Tempo indication token. 
   
   Assign to :class:`~abjad.Tempo` spanner ``indication``.
      
   ::

      abjad> t = Staff(construct.scale(4))
      abjad> tempo_spanner = Tempo(t[:])
      abjad> tempo_indication = TempoIndication(Rational(1, 8), 44)
      abjad> tempo_spanner.indication = tempo_indication

   ::

      abjad> print t.format
      \new Staff {
              \tempo 8=44
              c'8
              d'8
              e'8
              f'8
              %% tempo 8=44 ends here
      }
   '''

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

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self._dotted, self.mark)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dotted(self):
      '''Dotted numeral representation of duration.'''
      from abjad.note import Note
      return Note(0, self.duration).duration._dotted

   ## PUBLIC ATTRIBUTES ##

   @apply
   def duration( ):
      def fget(self):
         '''Duration of tempo indication.'''
         return self._duration
      def fset(self, arg):
         assert durtools.is_assignable(arg)
         self._duration = arg
      return property(**locals( ))

   @property
   def format(self):
      '''Tempo indication as string.'''
      return r'\tempo %s=%s' % (self._dotted, self.mark)

   @property
   def maelzel(self):
      '''Maelzel metronome marking.'''
      return Rational(1, 4) / self.duration * self.mark

   @apply
   def mark( ):
      def fget(self):
         '''Metronome mark value of tempo indication.'''
         return self._mark
      def fset(self, arg):
         assert isinstance(arg, (int, float))
         assert 0 < arg
         self._mark = arg
      return property(**locals( ))
