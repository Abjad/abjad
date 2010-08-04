from abjad.components.Container.multipliedduration import \
   _MultipliedContainerDurationInterface
from abjad.tools import mathtools
import types


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   r'''Manage duration attributes common to both fixed-duration
   and fixed-multiplier tuplets.
   '''

   def __init__(self, _client):
      '''Bind to client.
      Init as type of multiplied container duration interface.'''
      _MultipliedContainerDurationInterface.__init__(self, _client)
      self._preferred_denominator = None

   ## PRVIATE ATTRIBUTES ##

   @property
   def _binary(self):
      '''True when multiplier numerator is power of two,
      otherwise False.'''
      if self.multiplier:
         return mathtools.is_power_of_two(self.multiplier._n)
      else:
         return True
   
   @property
   def _multiplier_fraction_string(self):
      from abjad.tools import durtools
      if self.preferred_denominator is not None:
         d, n = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            ~self.multiplier, self.preferred_denominator)
      else:
         n, d = self.multiplier._n, self.multiplier._d
      return '%s/%s' % (n, d)

   @property
   def _nonbinary(self):
      return not self._binary

   ## PUBLIC ATTRIBUTES ##

   @property
   def augmentation(self):
      '''Read-only boolean. ``True`` when multiplier is
      greater than ``1``, otherwise ``False``.

      ::

         abjad> t = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.augmentation
         False
      '''

      if self.multiplier:
         return 1 < self.multiplier
      else:
         return False

   @property
   def diminution(self):
      '''Read-only boolean. ``True`` when multiplier is
      less than ``1``, otherwise ``False``.

      ::

         abjad> t = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.diminution
         True
      '''

      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @apply
   def preferred_denominator( ):
      def fget(self):
         '''.. versionadded:: 1.1.2
         Integer denominator in terms of which tuplet fraction
         should format.
         '''
         return self._preferred_denominator
      def fset(self, arg):
         if isinstance(arg, (int, long)):
            if not 0 < arg:
               raise ValueError
         elif not isinstance(arg, types.NoneType):
            raise TypeError
         self._preferred_denominator = arg
      return property(**locals( ))

   @property
   def preprolated(self):
      '''Read-only :class:`Rational <abjad.core.rational.Rational>`.
      Duration prior to prolation.

      ::

         abjad> t = FixedDurationTuplet((2, 8), macros.scale(3))
         abjad> t.duration.preprolated
         Rational(1, 4)
      '''

      return self.multiplied
