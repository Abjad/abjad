from abjad.container import Container
from abjad.exceptions import TupletFuseError
from abjad.rational import Rational
from abjad.tools import check
from abjad.tools import containertools
from abjad.tuplet import _Tuplet
from abjad.tuplet import FixedDurationTuplet
from abjad.tuplet import FixedMultiplierTuplet


def tuplets_by_reference(tuplets):
   r'''Fuse parent-contiguous `tuplets`::

      abjad> t1 = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> Beam(t1[:])
      abjad> t2 = FixedDurationTuplet((2, 16), construct.scale(3, Rational(1, 16)))
      abjad> Slur(t2[:])
      abjad> staff = Staff([t1, t2])
      abjad> f(staff)
      \new Staff {
         \times 2/3 {
            c'8 [
            d'8
            e'8 ]
         }
         \times 2/3 {
            c'16 (
            d'16
            e'16 )
         }
      }
      
   ::
      
      abjad> fuse.tuplets_by_reference(staff[:])
      FixedDurationTuplet(3/8, [c'8, d'8, e'8, c'16, d'16, e'16])

   ::

      abjad> f(staff)
      \new Staff {
         \times 2/3 {
            c'8 [
            d'8
            e'8 ]
            c'16 (
            d'16
            e'16 )
         }
      }

   Return new tuplet.

   Fuse zero or more parent-contiguous `tuplets`.

   Allow in-score `tuplets`.

   Allow outside-of-score `tuplets`.

   All `tuplets` must carry the same multiplier.

   All `tuplets` must be of the same type.
   '''

   from abjad.tools import scoretools

   check.assert_components(tuplets,
      klasses = (_Tuplet), contiguity = 'strict', share = 'parent')

   if len(tuplets) == 0:
      return None

   first = tuplets[0]
   first_multiplier = first.duration.multiplier
   first_type = type(first)
   for tuplet in tuplets[1:]:
      if tuplet.duration.multiplier != first_multiplier:
         raise TupletFuseError('tuplets must carry same multiplier.')
      if type(tuplet) != first_type:
         raise TupletFuseError('tuplets must be same type.')

   if isinstance(first, FixedDurationTuplet):
      total_contents_duration = sum([x.duration.contents for x in tuplets])
      new_target_duration = first_multiplier * total_contents_duration
      new_tuplet = FixedDurationTuplet(new_target_duration, [ ])
   elif isinstance(first, FixedMultiplierTuplet):
      new_tuplet = FixedMultiplierTuplet(first_multiplier, [ ])
   else:
      raise TypeError('unknown tuplet type.')

   wrapped = False
   if tuplets[0].parentage.root is not tuplets[-1].parentage.root:
      dummy_container = Container(tuplets) 
      wrapped = True
   scoretools.donate(tuplets, new_tuplet)

   if wrapped:
      containertools.contents_delete(dummy_container)
   
   return new_tuplet
