from abjad.tools import durtools
from abjad.tools.marktools.Mark import Mark
from fractions import Fraction


class TempoMark(Mark):
   '''.. versionadded:: 1.1.2

   Tempo mark.
   '''

   _format_slot = 'opening'

   def __init__(self, *args):
      Mark.__init__(self)
      if len(args) == 1 and isinstance(args[0], type(self)):
         tempo_indication = args[0]
         duration = Fraction(tempo_indication.duration)
         units_per_minute = tempo_indication.units_per_minute
      elif len(args) == 2:
         duration, units_per_minute = args
         assert isinstance(duration, Fraction)
         assert isinstance(units_per_minute, (int, long, float, Fraction))
         duration = duration
         units_per_minute = units_per_minute
      else:
         raise ValueError('can not initialize tempo indication.')
      object.__setattr__(self, '_duration', duration)
      object.__setattr__(self, '_units_per_minute', units_per_minute)

   ## OVERLOADS ##

   def __add__(self, expr):
      if isinstance(expr, type(self)):
         new_quarters_per_minute = self.quarters_per_minute + expr.quarters_per_minute
         minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
         new_units_per_minute, new_duration_denominator = \
            durtools.rational_to_duration_pair_with_specified_integer_denominator(
            new_quarters_per_minute / 4, minimum_denominator)
         new_duration = Fraction(1, new_duration_denominator)
         new_tempo_indication = type(self)(new_duration, new_units_per_minute)
         return new_tempo_indication

   def __div__(self, expr):
      if isinstance(expr, type(self)):
         return self.quarters_per_minute / expr.quarters_per_minute
      raise TypeError('must be tempo indication.')

   def __eq__(self, expr):
      if isinstance(expr, type(self)):
         if self.duration == expr.duration:
            if self.units_per_minute == expr.units_per_minute:
               return True
      return False

   def __mul__(self, multiplier):
      if isinstance(multiplier, (int, float, Fraction)):
         new_units_per_minute = multiplier * self.units_per_minute
         new_duration = Fraction(self.duration)
         new_tempo_indication = type(self)(new_duration, new_units_per_minute)
         return new_tempo_indication

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      return '%s(%s, %s)' % (
         self.__class__.__name__, self._dotted, self.units_per_minute)

   def __sub__(self, expr):
      if isinstance(expr, type(self)):
         new_quarters_per_minute = self.quarters_per_minute - expr.quarters_per_minute
         minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
         new_units_per_minute, new_duration_denominator = \
            durtools.rational_to_duration_pair_with_specified_integer_denominator(
            new_quarters_per_minute / 4, minimum_denominator)
         new_duration = Fraction(1, new_duration_denominator)
         new_tempo_indication = type(self)(new_duration, new_units_per_minute)
         return new_tempo_indication

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dotted(self):
      '''Dotted numeral representation of duration.'''
      return durtools.assignable_rational_to_lilypond_duration_string(self.duration)

   @property
   def _equation(self):
      '''Dotted numeral and units per minute together around equal sign.'''
      return '%s=%s' % (self._dotted, self.units_per_minute)

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      '''Duration of tempo indication.'''
      return self._duration

   @property
   def format(self):
      '''Tempo indication as string.'''
      return r'\tempo %s' % self._equation

   @property
   def quarters_per_minute(self):
      '''Read-only number of quarters per minute.'''
      return Fraction(1, 4) / self.duration * self.units_per_minute

   @property
   def units_per_minute(self):
      '''Units per minute of tempo indication.'''
      return self._units_per_minute
