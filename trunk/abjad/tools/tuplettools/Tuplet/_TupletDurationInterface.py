from abjad.components.Container._MultipliedContainerDurationInterface import _MultipliedContainerDurationInterface
from abjad.tools import mathtools
from abjad.tools import durtools
import fractions


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   r'''Manage duration attributes common to both fixed-duration and fixed-multiplier tuplets.
   '''

   def __init__(self, _client, multiplier):
      _MultipliedContainerDurationInterface.__init__(self, _client)
      self._preferred_denominator = None
      self.multiplier = multiplier

   ## PRVIATE ATTRIBUTES ##

   @property
   def _duration(self):
      if 0 < len(self._client):
         return self.multiplier * self.contents
      else:
         return durtools.Duration(0)

   @property
   def _multiplier_fraction_string(self):
      from abjad.tools import durtools
      if self.preferred_denominator is not None:
         inverse_multiplier = fractions.Fraction(self.multiplier.denominator, self.multiplier.numerator)
         d, n = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            inverse_multiplier, self.preferred_denominator)
      else:
         n, d = self.multiplier.numerator, self.multiplier.denominator
      return '%s/%s' % (n, d)

   ## PUBLIC ATTRIBUTES ##

   @property
   def is_augmentation(self):
      '''True when multiplier is greater than 1.
      Otherwise false::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
         abjad> t.duration.is_augmentation
         False

      Return boolean.
      '''
      if self.multiplier:
         return 1 < self.multiplier
      else:
         return False

   @property
   def is_binary(self):
      '''True when multiplier numerator is power of two, otherwise False.
      '''
      if self.multiplier:
         return mathtools.is_nonnegative_integer_power_of_two(self.multiplier.numerator)
      else:
         return True
   
   @property
   def is_diminution(self):
      '''True when multiplier is less than 1.
      Otherwise false::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
         abjad> t.duration.is_diminution
         True
   
      Return boolean.
      '''
      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @property
   def is_nonbinary(self):
      return not self.is_binary

   @property
   def multiplied(self):
      return self.multiplier * self.contents

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = fractions.Fraction(expr)
         elif isinstance(expr, tuple):
            rational = fractions.Fraction(*expr)
         elif isinstance(expr, fractions.Fraction):
            rational = fractions.Fraction(expr)
         else:
            raise ValueError('can not set tuplet multiplier: "%s".' % str(expr))
         if 0 < rational:
            self._multiplier = rational
         else:
            raise ValueError('tuplet multiplier must be positive: "%s".' % rational)
      return property(**locals( ))

   @apply
   def preferred_denominator( ):
      def fget(self):
         '''.. versionadded:: 1.1.2
         Integer denominator in terms of which tuplet fraction should format.
         '''
         return self._preferred_denominator
      def fset(self, arg):
         if isinstance(arg, (int, long)):
            if not 0 < arg:
               raise ValueError('tuplet preferred denominator must be positive: "%s".' % arg)
         elif not isinstance(arg, type(None)):
            raise TypeError('bad tuplet preferred denominator type: "%s".' % arg)
         self._preferred_denominator = arg
      return property(**locals( ))

   @property
   def preprolated(self):
      '''Duration prior to prolation:

      ::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
         abjad> t.duration.preprolated
         Duration(1, 4)

      Return duration.
      '''
      return self.multiplied
