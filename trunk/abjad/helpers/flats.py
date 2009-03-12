from abjad.helpers.iterate import iterate
from abjad.helpers.pitch_renotate_flats import pitch_renotate_flats
from abjad.pitch.pitch import Pitch


def flats(expr):
   from abjad.leaf.leaf import _Leaf
   if isinstance(expr, Pitch):
      pitch_renotate_flats(expr)
   else:
      for leaf in iterate(expr, _Leaf):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               pitch_renotate_flats(pitch)
