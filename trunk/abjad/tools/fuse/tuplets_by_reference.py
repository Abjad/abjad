from abjad.container import Container
from abjad.exceptions import TupletFuseError
from abjad.rational import Rational
from abjad.tools import check
from abjad.tools import containertools
from abjad.tuplet import _Tuplet
from abjad.tuplet import FixedDurationTuplet
from abjad.tuplet import FixedMultiplierTuplet


def tuplets_by_reference(tuplets):
   '''Fuse zero or more tuplets in the 'tuplets' list.
   Tuplets to fuse must carry the same multiplier.
   Tuplets to fuse must be of the same type.
   Works on in-score and outside-of-score tuplets.
   Returns newly instantiated, fused tuplet.
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
