from abjad.exceptions.exceptions import TupletFuseError
from abjad.rational.rational import Rational
from abjad.tools import check
from abjad.tools import parenttools
from abjad.tools.parenttools.switch import _switch
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to
from abjad.tuplet.tuplet import _Tuplet
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


def tuplets_by_reference(tuplets):
   '''Fuse zero or more tuplets in the 'tuplets' list.
      Tuplets to fuse must carry the same multiplier.
      Tuplets to fuse must be of the same type.
      Works on in-score and outside-of-score tuplets.
      Returns newly instantiated, fused tuplet.'''

   check.assert_components(tuplets,
      klasses = (_Tuplet), contiguity = 'strict', share = 'parent')

   if len(tuplets) == 0:
      return None

   parent, start, stop = parenttools.get_with_indices(tuplets)

   first = tuplets[0]
   first_multiplier = first.duration.multiplier
   first_type = type(first)
   for tuplet in tuplets[1:]:
      if tuplet.duration.multiplier != first_multiplier:
         raise TupletFuseError('tuplets must carry same multiplier.')
      if type(tuplet) != first_type:
         raise TupletFuseError('tuplets must be same type.')

   new_music = [ ]
   total_contents_duration = Rational(0)
   for tuplet in tuplets:
      total_contents_duration += tuplet.duration.contents
      tuplet_music = tuplet[:]
      _switch(tuplet_music, None)
      new_music += tuplet_music

   if isinstance(first, FixedDurationTuplet):
      new_target_duration = first_multiplier * total_contents_duration
      new_tuplet = FixedDurationTuplet(new_target_duration, new_music)
   elif isinstance(first, FixedMultiplierTuplet):
      new_tuplet = FixedMultiplierTuplet(first_multiplier, new_music)
   else:
      raise TypeError('unknown tuplet type.')

   if parent is not None:
      _give_dominant_to(tuplets, [new_tuplet])

   _switch(tuplets, None)
   if parent is not None:
      parent.insert(start, new_tuplet)

   return new_tuplet
