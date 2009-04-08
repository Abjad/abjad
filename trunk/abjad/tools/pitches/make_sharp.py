from abjad.tools import iterate
from abjad.helpers.pitch_renotate_sharps import pitch_renotate_sharps
from abjad.pitch.pitch import Pitch


def make_sharp(expr):
   if isinstance(expr, Pitch):
      pitch_renotate_sharps(expr)
   else:
      from abjad.leaf.leaf import _Leaf
      for leaf in iterate.naive(expr, _Leaf):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               pitch_renotate_sharps(pitch)
