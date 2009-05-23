from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational
from abjad.tempo.indication import TempoIndication


class SpacingIndication(_Abjad):
   '''Spacing indication token.
      This says that LilyPond Score.proportionalNotationDuration
      should equal ``proportional_notation_duration`` when tempo
      is equal to ``tempo_indication``.

      Example::

         abjad> tempo = TempoIndication(Rational(1, 8), 44)
         abjad> spacing_indication = SpacingIndication(tempo, Rational(1, 68))
         abjad> spacing_indication
         <SpacingIndication>'''

   def __init__(self, tempo_indication, proportional_notation_duration):
      '''Initialize ``tempo_indication`` and 
         ``proportional_notation_duration``.'''
      self.tempo_indication = tempo_indication
      self.proportional_notation_duration = proportional_notation_duration
      
   ## OVERLOADS ##

   def __eq__(self, expr):
      '''Spacing indications compare equal when
         normalized spacing durations compare equal.'''
      if isinstance(expr, SpacingIndication):
         if self.normalized_spacing_duration == \
            expr.normalized_spacing_duration:
            return True
      return False

   def __ne__(self, expr):
      '''Spacing indications compare unequal when
         normalized spacing durations compare unequal.'''
      return not self == expr

   ## PUBLIC ATTRIBUTES ##

   @property
   def normalized_spacing_duration(self):
      '''Read-only proportional notation duration at 60 MM.'''
      indication = self.tempo_indication
      duration = self.proportional_notation_duration
      scalar = indication.duration / indication.mark * 60 / Rational(1, 4)
      return scalar * self.proportional_notation_duration

   @apply
   def proportional_notation_duration( ):
      '''Read / write LilyPond proportionalNotationDuration.'''
      def fget(self):
         return self._proportional_notation_duration
      def fset(self, expr):
         assert isinstance(expr, Rational)
         assert 0 < expr
         self._proportional_notation_duration = expr

   @apply
   def tempo_indication( ):
      '''Read / write Abjad ``TempoIndication``.'''
      def fget(self):
         return self._tempo_indication
      def fset(self, expr):
         assert isinstance(expr, TempoIndication)
         self._tempo_indication = expr
      return property(**locals( ))
