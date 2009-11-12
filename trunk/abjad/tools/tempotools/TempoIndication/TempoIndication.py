from abjad.core.abjadcore import _Abjad
from abjad.tools import durtools
from abjad.rational import Rational


class TempoIndication(_Abjad):
   r'''Tempo indication token. 
   
   Assign to :class:`~abjad.TempoSpanner` spanner ``indication``. ::

      abjad> t = Staff(construct.scale(4))
      abjad> tempo_spanner = TempoSpanner(t[:])
      abjad> tempo_indication = TempoIndication(Rational(1, 8), 44)
      abjad> tempo_spanner.tempo_indication = tempo_indication

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

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], TempoIndication):
         tempo_indication = args[0]
         self.duration = Rational(tempo_indication.duration)
         self.units_per_minute = tempo_indication.units_per_minute
      elif len(args) == 2:
         duration, units_per_minute = args
         assert isinstance(duration, Rational)
         assert isinstance(units_per_minute, (int, long, float))
         self.duration = duration
         self.units_per_minute = units_per_minute
      else:
         raise ValueError('can not initialize tempo indication.')

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, TempoIndication):
         if self.duration == expr.duration:
            if self.units_per_minute == expr.units_per_minute:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      return '%s(%s, %s)' % (
         self.__class__.__name__, self._dotted, self.units_per_minute)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dotted(self):
      '''Dotted numeral representation of duration.'''
      from abjad.note import Note
      return Note(0, self.duration).duration._dotted

   @property
   def _equation(self):
      '''Dotted numeral and units per minute together around equal sign.'''
      return '%s=%s' % (self._dotted, self.units_per_minute)

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
      return r'\tempo %s' % self._equation

   @property
   def quarters_per_minute(self):
      '''Read-only number of quarters per minute.'''
      return Rational(1, 4) / self.duration * self.units_per_minute

   @apply
   #def mark( ):
   def units_per_minute( ):
      def fget(self):
         '''Units per minute.'''
         return self._units_per_minute
      def fset(self, arg):
         assert isinstance(arg, (int, float))
         assert 0 < arg
         self._units_per_minute = arg
      return property(**locals( ))
