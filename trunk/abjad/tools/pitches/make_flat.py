from abjad.pitch.pitch import Pitch
from abjad.tools import iterate


def make_flat(expr):
   from abjad.leaf.leaf import _Leaf
   if isinstance(expr, Pitch):
      _pitch_renotate_flats(expr)
   else:
      for leaf in iterate.naive(expr, _Leaf):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_flats(pitch)


def _pitch_renotate_flats(pitch):
   octave = pitch.tools.pitchNumberToOctave(pitch.number)
   name = pitch.tools.pcToPitchNameFlats[pitch.pc]
   pitch.octave = octave
   pitch.name = name
