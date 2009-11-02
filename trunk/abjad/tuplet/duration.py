from abjad.container.multipliedduration import \
   _MultipliedContainerDurationInterface
from abjad.tools import mathtools


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   r'''Manage duration attributes common to both fixed-duration
   and fixed-multiplier tuplets.
   '''

   def __init__(self, _client):
      '''Bind to client.
      Init as type of multiplied container duration interface.'''
      _MultipliedContainerDurationInterface.__init__(self, _client)

   ## PRVIATE ATTRIBUTES ##

   @property
   def _binary(self):
      '''True when multiplier numerator is power of two,
      otherwise False.'''
      if self.multiplier:
         return mathtools.is_power_of_two(self.multiplier._n)
      else:
         return True

   ## PUBLIC ATTRIBUTES ##

   @property
   def augmentation(self):
      '''Read-only boolean. ``True`` when multiplier is
      greater than ``1``, otherwise ``False``.

      ::

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
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

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
         abjad> t.duration.diminution
         True
      '''

      if self.multiplier:
         return self.multiplier < 1
      else:
         return False

   @property
   def preprolated(self):
      '''Read-only :class:`Rational <abjad.rational.rational.Rational>`.
      Duration prior to prolation.

      ::

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
         abjad> t.duration.preprolated
         Rational(1, 4)
      '''

      return self.multiplied
