from abjad.components.Container._MultipliedContainerDurationInterface import _MultipliedContainerDurationInterface
from abjad.tools import mathtools
from fractions import Fraction


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   r'''Manage duration attributes common to both fixed-duration and fixed-multiplier tuplets.
   '''

   #def __init__(self, _client):
   def __init__(self, _client, multiplier):
      _MultipliedContainerDurationInterface.__init__(self, _client)
      self._preferred_denominator = None
      ## new ##
      self.multiplier = multiplier

   ## PRVIATE ATTRIBUTES ##

   ## new ##
   @property
   def _duration(self):
      if 0 < len(self._client):
         return self.multiplier * self.contents
      else:
         return Fraction(0)

   @property
   def _multiplier_fraction_string(self):
      from abjad.tools import durtools
      if self.preferred_denominator is not None:
         #d, n = durtools.rational_to_duration_pair_with_specified_integer_denominator(
         #   ~self.multiplier, self.preferred_denominator)
         inverse_multiplier = Fraction(self.multiplier.denominator, self.multiplier.numerator)
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

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.is_augmentation
         False
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
         return mathtools.is_power_of_two(self.multiplier.numerator)
      else:
         return True
   
   @property
   def is_diminution(self):
      '''True when multiplier is less than 1.
      Otherwise false::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.is_diminution
         True
      '''

      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @property
   def is_nonbinary(self):
      return not self.is_binary

   ## new ##
   @property
   def multiplied(self):
      return self.multiplier * self.contents

   ## new ##
   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = Fraction(expr)
         elif isinstance(expr, tuple):
            rational = Fraction(*expr)
         elif isinstance(expr, Fraction):
            rational = Fraction(expr)
         else:
            raise ValueError('Can not set tuplet rational from %s.' % str(expr))
         if 0 < rational:
            self._multiplier = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' % rational)
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
               raise ValueError
         elif not isinstance(arg, type(None)):
            raise TypeError
         self._preferred_denominator = arg
      return property(**locals( ))

   @property
   def preprolated(self):
      '''Duration prior to prolation:

      ::

         abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.preprolated
         Fraction(1, 4)
      '''

      return self.multiplied
