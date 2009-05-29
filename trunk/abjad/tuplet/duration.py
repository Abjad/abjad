from abjad.container.multipliedduration import \
   _MultipliedContainerDurationInterface
from abjad.tools import mathtools


class _TupletDurationInterface(_MultipliedContainerDurationInterface):
   r'''Manage duration attributes common to both \
      :class:`FixedDurationTuplet \
      <abjad.tuplet.fd.tuplet.FixedDurationTuplet>` and \
      :class:`FixedMultiplierTuplet \
      <abjad.tuplet.fm.tuplet.FixedMultiplierTuplet>`.

      *  This is an abstract base class that never instantiates explicitly.
      *  Both :class:`_FDTupletDurationInterface \
         <abjad.tuplet.fd.duration._FDTupletDurationInterface>` and \
         :class:`_FMTupletDurationInterface \
         <abjad.tuplet.fm.duration._FMTupletDurationInterface>` \
         inherit from this class.
      *  Both are concrete classes that do instantiate explicitly.
      *  For these reasons, the examples here show tuplets with \
         :class:`_FDTupletDurationInterface \
         <abjad.tuplet.fd.duration._FDTupletDurationInterface>`.

      ::

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))

         abjad> print t.format
         \times 2/3 {
            c'8
            d'8
            e'8
         }

         abjad> t.duration
         <_FDTupletDurationInterface>'''

   def __init__(self, _client):
      '''Bind to client.
         Init as type of multiplied container duration interface.'''
      _MultipliedContainerDurationInterface.__init__(self, _client)

   ### PRVIATE ATTRIBUTES ###

   @property
   def _binary(self):
      '''``True`` when multiplier numerator is power of two, \
            otherwise ``False``.'''
      if self.multiplier:
         return mathtools.is_power_of_two(self.multiplier._n)
      else:
         return True

   ### PUBLIC ATTRIBUTES ###

   @property
   def augmentation(self):
      '''Read-only boolean. ``True`` when multiplier is \
         greater than ``1``, otherwise ``False``.

         ::

            abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
            abjad> t.duration.augmentation
            False'''

      if self.multiplier:
         return 1 < self.multiplier
      else:
         return False

   @property
   def diminution(self):
      '''Read-only boolean. ``True`` when multiplier is \
         less than ``1``, otherwise ``False``.

         ::

            abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
            abjad> t.duration.diminution
            True'''

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
            Rational(1, 4)'''

      return self.multiplied
